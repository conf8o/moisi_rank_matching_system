from dataclasses import dataclass
from numbers import Number
from enum import Enum
from collections import deque
from abc import ABC

@dataclass
class Player:
    """
    選手
    """

    id: str
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

    def __init__(self, players: list[Player]) -> None:
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


class SoloMatching:
    def __init__(self, entries: list[Entry], median: Number) -> None:
        self.entries = list(sorted(entries, key=Entry.sort_key))
        self.median = median
        self.players = [entry.players[0] for entry in self.entries]

    def make_match(self) -> list[Entry]:
        """
        [3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 6, 7, 7, 7]: len = 13, split_len = 13 // 3 = 4 
        
        lower: sorted asc
        [3, 3, 3, 4]

        higher: sorted desc 
        [7, 7, 7, 6]
        
        mid: deque
        [4, 4, 5, 6, 6, 6]
        
        midの内部レートに応じて、lowerとhigherのペアを取ってくる
        """

        l = len(self.players)
        if l < 3:
            return self.entries
        
        split_l = l // 3
        lowers = self.players[:split_l]
        highers = sorted(self.players[-split_l:], key=lambda x: -x.inner_rate)
        
        matchings = []
        pairs = deque(sorted(zip(lowers, highers), key=lambda x: Entry([*x]).inner_rate))
        mids = iter(self.players[split_l:-split_l])
        for mid in mids:
            if mid.inner_rate >= self.median:
                lower, higher = pairs.popleft()
                matchings.append(Entry([lower, mid, higher]))
            else:
                lower, higher = pairs.pop()
                matchings.append(Entry([lower, mid, higher]))

            if not pairs:
                break
        
        mids = list(mids)
        if mids:
            rest = Entry(list(mids))
            matchings.append(rest)
        
        return matchings


def _median(entries: list[Entry]) -> Number:
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
    @staticmethod
    def make_trio(duo: Entry, solo: Entry) -> Entry:
        return Entry([duo.players[0], duo.players[1], solo.players[0]])

    def __init__(self, entries: list[Entry], median: Number) -> None:
        self.entries = sorted(entries, key=Entry.sort_key)
        self.median = median
        self.solos = deque(filter(Entry.is_solo, self.entries))
        self.duos = list(filter(Entry.is_duo, self.entries))

    def make_match(self) -> list[Entry]:
        matchings = []
        for duo in self.duos:
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
        return matchings


class Matching:
    def __init__(self, entries: list[Entry]) -> None:
        self.entries = sorted(entries, key=Entry.sort_key)
        self.median = _median(self.entries)
        self.solos = list(filter(Entry.is_solo, self.entries))
        self.duos = list(filter(Entry.is_duo, self.entries))
        self.trios = list(filter(Entry.is_trio, self.entries))

    def make_match(self) -> list[Entry]:
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

    def __init__(self, players: list[Player]) -> None:
        if len(players) > Party.MAX_LEN:
            raise PartyMaxLenError()
        
        self.players = players
    
    @property
    def inner_rate(self) -> int:
        return sum(player.inner_rate for player in self.players) / Party.MAX_LEN
    

@dataclass
class Match:
    id: str
    parties: list[Party]


class AMatchRepository(ABC):
    def __init__(self, store) -> None:
        self.store = store

    def save(self, payload: Match) -> Match:
        return payload
