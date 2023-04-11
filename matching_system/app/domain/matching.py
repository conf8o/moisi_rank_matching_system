from dataclasses import dataclass
from numbers import Number
from enum import Enum
from collections import deque
from abc import ABC
from typing import List
import heapq

@dataclass
class Player:
    """
    選手
    """

    id: int
    name: str
    point: int

    @property
    def inner_rate(self) -> int:
        return self.point


class EntryMaxLexError(Exception):
    pass


class Entry:
    """
    エントリー。マッチングする前のパーティ情報。ソロでもデュオでもトリオでもこれ
    """

    MAX_LEN = 3

    def __init__(self, players: List[Player]) -> None:
        if len(players) > Entry.MAX_LEN:
            raise EntryMaxLexError()
    
        self.players = players

    def is_solo(self) -> bool:
        return len(self.players) == 1
    
    def is_duo(self) -> bool:
        return len(self.players) == 2
    
    def is_trio(self) -> bool:
        return len(self.players) == 3

    @property
    def inner_rate(self) -> int:
        return sum(p.inner_rate for p in self.players) / len(self.players)

    def sort_key(self) -> tuple[int]:
        return [self.inner_rate, *sorted(p.inner_rate for p in self.players)]
    
    def __repr__(self) -> str:
        return f"Entry({self.players})"



def _median(entries: List[Entry]) -> Number:
    """
    [1, 2, 3, 4] -> 2.5
    [1, 2, 3] -> 2
    """

    if not entries:
        return 0
    
    l = len(entries)
    if l % 2 == 0:
        return (entries[l//2].inner_rate + entries[l//2-1].inner_rate) / 2
    else:
        return entries[l//2].inner_rate

class DuoMatchingError(Exception):
    pass


class DuoMatching:
    class Priority:
        def __init__(self, entry: Entry, median: Number) -> None:
            self.entry = entry
            self.median = median

        def __lt__(self, other: 'DuoMatching.Priority'):
            return -abs(self.entry.inner_rate - self.median) < -abs(other.entry.inner_rate - other.median)

    @staticmethod
    def make_trio(duo: Entry, solo: Entry) -> Entry:
        return Entry([duo.players[0], duo.players[1], solo.players[0]])

    def __init__(self, entries: List[Entry], median: Number) -> None:
        self.entries = sorted(entries, key=Entry.sort_key)
        self.median = median
        self.solos = deque(filter(Entry.is_solo, self.entries))
        self.duos = list(filter(Entry.is_duo, self.entries))
        self.duos_for_heap = [DuoMatching.Priority(e, self.median) for e in self.duos]
        heapq.heapify(self.duos_for_heap)

    def make_match(self) -> List[Entry]:
        matchings = []
        while self.duos_for_heap:
            duo = heapq.heappop(self.duos_for_heap).entry
            if duo.inner_rate >= self.median:
                solo = self.solos.popleft()
                matchings.append(DuoMatching.make_trio(duo, solo))
            else:
                solo = self.solos.pop()
                matchings.append(DuoMatching.make_trio(duo, solo))

            if not self.solos:
                break

        if self.solos:
            matchings += list(self.solos)

        if self.duos_for_heap:
            matchings += [e.entry for e in self.duos_for_heap]
    
        return matchings
    

class SoloMatching:
    def __init__(self, entries: List[Entry], median: Number) -> None:
        self.entries = list(sorted(entries, key=Entry.sort_key))
        self.median = median
        self.players = [entry.players[0] for entry in self.entries]

    def make_match(self) -> List[Entry]:
        l = len(self.players)
        if l < 3:
            return self.entries
        
        split_l = l // 3
        lowers = self.players[:split_l]
        highers = sorted(self.players[-split_l:], key=lambda x: -x.inner_rate)
        
        pairs = [Entry([*p]) for p in zip(lowers, highers)]
        mids = [Entry([s]) for s in self.players[split_l:-split_l]]
        mid_strongers = []
        while len(mids) - split_l > 0:
            mid_strongers.append(mids.pop())

        duo_matching = DuoMatching(pairs + mids, self.median)
        matchings = duo_matching.make_match()
        
        res = list(filter(Entry.is_trio, matchings))
        if mid_strongers:
            rest = Entry(mid_strongers)
            res.append(rest)
        
        return res 


class Matching:
    def __init__(self, entries: List[Entry]) -> None:
        self.entries = sorted(entries, key=Entry.sort_key)
        self.median = _median(self.entries)
        self.solos = list(filter(Entry.is_solo, self.entries))
        self.duos = list(filter(Entry.is_duo, self.entries))
        self.trios = list(filter(Entry.is_trio, self.entries))

    def make_match(self) -> List[Entry]:
        duo_matching = DuoMatching(self.solos + self.duos, self.median)
        duo_matching_results = duo_matching.make_match()

        trios = list(filter(Entry.is_trio, duo_matching_results))
        rest_solos = list(filter(Entry.is_solo, duo_matching_results))

        matchings = self.trios + trios
        if not rest_solos:
            return matchings
        else:
            solo_matching = SoloMatching(rest_solos, self.median)
            return matchings + solo_matching.make_match()


class PartyMaxLenError(Exception):
    pass


class Party:
    """
    マッチングで確定したパーティ情報。
    """

    MAX_LEN = 3

    def __init__(self, players: List[Player]) -> None:
        if len(players) > Party.MAX_LEN:
            raise PartyMaxLenError()
        
        self.players = players
    
    @property
    def inner_rate(self) -> int:
        return sum(player.inner_rate for player in self.players) / Party.MAX_LEN
    

@dataclass
class Match:
    id: int
    parties: List[Party]


class AMatchRepository(ABC):
    def __init__(self, store) -> None:
        self.store = store

    def save(self, payload: Match) -> Match:
        ...
