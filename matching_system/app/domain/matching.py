from dataclasses import dataclass

@dataclass
class Player:
    """
    選手
    """

    id: str
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


def calculate_matching(players: list[Entry]) -> Matching:
    return False
