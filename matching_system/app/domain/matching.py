from dataclasses import dataclass

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

class Entry:
    """
    エントリー。マッチングする前のパーティ情報。ソロでもデュオでもトリオでもこれ
    """

    MAX_LEN = 3

    def __init__(self, players: list[Player]) -> None:
        if len(players) > Entry.MAX_LEN:
            raise PartyMaxLenError()
        
        self.players = players

    @property
    def inner_rate(self) -> int:
        return sum(p.inner_rate for p in self.players) / len(self.players)

    def sort_key(self) -> tuple[int]:
        return [self.inner_rate, *sorted(p.inner_rate for p in self.players)]
    
    def __repr__(self) -> str:
        return f"Entry({self.players})"


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
class Matching:
    parties: list[Party]


class SoloMatching:
    def __init__(self, entries: list[Entry]) -> None:
        self.entries = list(sorted(entries, key=Entry.sort_key))
        self.players = [entry.players[0] for entry in self.entries]

    def make_match(self) -> list[Entry]:
        """
        [3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 6, 7, 7, 7]: len = 13, split_len = 13 // 3 = 4 
        
        matching_queues:
        [3, 3, 3, 4] lower sorted asc
        [7, 7, 7, 6] higher sorted desc
        [4, 4, 5, 6] mid sorted asc
        
        ↑ 列でマッチ
        rest: [6, 6]
        """

        l = len(self.players)
        if l < 3:
            return self.entries
        
        split_l = l // 3
        lower = self.players[:split_l]
        higher = sorted(self.players[split_l:], key=lambda x: -x.inner_rate)
        
        mid = self.players[split_l:-split_l]
        rest = [] if split_l == len(mid) else [Entry(mid[split_l:])]
        mid = mid[:split_l]

        matchings = [Entry(list(trio)) for trio in zip(lower, higher, mid)]

        return matchings + rest


def lowers(entries):
    return entries[:len(entries)//2]
    

def highers(entries):
    return entries[len(entries)//2:]
    
class DuoMatching:
    def make_trio(duo: Entry, solo: Entry) -> Entry:
        return Entry([duo.players[0], duo.players[1], solo.players[0]])

    def __init__(self, entries: list[Entry]) -> None:
        self.entries = sorted(entries, key=Entry.sort_key)

        self.solos = [entry for entry in self.entries if len(entry.players) == 1]
        self.duos = [entry for entry in self.entries if len(entry.players) == 2]

        self.lower_solos = lowers(self.solos)
        self.higher_solos = highers(self.solos)
        self.lower_duos = lowers(self.duos)
        self.higher_duos = highers(self.duos)


    def make_match(self) -> list[Entry]:
        """
        entries:
            [[2], [2], [2, 2], [3], [2, 4], [3, 3], [5]]
        
        1. lower_duo_matching:
            [[2, 2], [3], [5]]
        2. higher_duo_matching:
            [[2], [2], [2, 4], [3, 3]]
        
        1-1. lower_duo_matching:
            [[2, 2, 5], [3]]
        1-2. higher_duo_matching:
            pass
            
        2-1. lower_duo_matching:
            [[2, 4, 2]]
        2-2. higher_duo_matching:
            [[3, 3, 2]]
        """

        matchings = []

        # lower_duo_matching
        if len(self.lower_duos) == 1:
            solo = self.higher_solos[-1]
            solos = [] if len(self.higher_solos) == 1 else self.higher_solos[:-1]
            trio = DuoMatching.make_trio(self.lower_duos[0], solo)
            matchings += [trio, *solos]
        else:
            if not self.lower_duos:
                matchings += self.higher_solos
            elif not self.higher_solos:
                matchings += self.lower_duos
            else:
                lower_duo_matching = DuoMatching(self.lower_duos + self.higher_solos)
                matchings += lower_duo_matching.make_match()
        
        # higher_duo_matching
        if len(self.higher_duos) == 1:
            solo = self.lower_solos[0]
            solos = [] if len(self.lower_solos) == 1 else self.lower_solos[1:]
            trio = DuoMatching.make_trio(self.higher_duos[0], solo)
            matchings += [trio, *solos]
        else:
            if not self.higher_duos:
                matchings += self.lower_solos
            elif not self.lower_solos:
                matchings += self.higher_duos
            else:
                higher_duo_matching = DuoMatching(self.higher_duos + self.lower_solos)
                matchings += higher_duo_matching.make_match()

        return matchings
