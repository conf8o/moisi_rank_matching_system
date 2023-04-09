from domain.matching import AMatchRepository, Matching, Party, Entry, Match
from typing import List

class MockMatchRepository(AMatchRepository):
    pass

def make_match(store: AMatchRepository, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match("uuid", parties)
    return store.save(payload)


def parties_from_entries(entries: List[Entry]) -> List[Party]:
    return [Party(e.players[:]) for e in entries]
