from app.domain.matching import AMatchRepository, Matching, Party, Entry, Match


class MockMatchRepository(AMatchRepository):
    pass

def make_match(store: AMatchRepository, entries: list[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match("uuid", parties)
    return store.save(payload)


def parties_from_entries(entries: list[Entry]) -> list[Party]:
    return [Party(e.players[:]) for e in entries]
