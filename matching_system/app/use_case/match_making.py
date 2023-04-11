from domain.matching import AMatchRepository, Matching, Party, Entry, Match
from typing import List
from sqlalchemy.orm import Session
from infra.matching import MatchRepository


class ProtoMatchRepository(AMatchRepository):
    pass

def make_match(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match("uuid", parties)
    return MatchRepository(db).save(payload)


def make_match_proto(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match("uuid", parties)
    return ProtoMatchRepository(db).save(payload)


def parties_from_entries(entries: List[Entry]) -> List[Party]:
    return [Party(e.players[:]) for e in entries]
