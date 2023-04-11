from domain.matching import AMatchRepository, Matching, Party, Entry, Match, Player
from typing import List
from sqlalchemy.orm import Session
from infra.matching import MatchRepository
from uuid import uuid4

class ProtoMatchRepository(AMatchRepository):
    pass

def make_match(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(str(uuid4()), parties)
    return MatchRepository(db).save(payload)


def make_match_proto(db: Session, entries: List[Entry]) -> Match:
    matching = Matching(entries)
    parties = parties_from_entries(matching.make_match())
    payload = Match(str(uuid4()), parties)
    return ProtoMatchRepository(db).save(payload)


def parties_from_entries(entries: List[Entry]) -> List[Party]:
    def player_with_new_id(p: Player):
        id = str(uuid4())
        return Player(id, p.name, p.point)
    
    return [Party(str(uuid4()), [player_with_new_id(p) for p in e.players]) for e in entries]
