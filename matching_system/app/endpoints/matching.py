from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from use_case import match_making
from domain import matching as domain
from pydantic import BaseModel


router = APIRouter()


class Player(BaseModel):
    id: str
    name: str
    point: int
    
    def to_model(self) -> domain.Player:
        return domain.Player(self.id, self.name, self.point)
    
    def from_model(player: domain.Player) -> 'Player':
        return Player(id=player.id, name=player.name, point=player.point)


class Entry(BaseModel):
    players: List[Player]

    def to_model(self) -> domain.Entry:
        return domain.Entry([p.to_model() for p in self.players])

class Party(BaseModel):
    players: List[Player]

    @staticmethod
    def from_model(party: domain.Party) -> 'Party':
        return Party(players=[Player.from_model(p) for p in party.players])


class MatchMakingRequest(BaseModel):
    entries: List[Entry]

    def to_model(self) -> List[domain.Entry]:
        return [e.to_model() for e in self.entries]


class MatchMakingResponse(BaseModel):
    parties: List[Party]

    @staticmethod
    def from_model(parties: List[domain.Party]) -> 'MatchMakingResponse':
        return MatchMakingResponse(parties=[Party.from_model(p) for p in parties])


@router.post("/entries")
def create_entry(db: Session = Depends(get_db)):
    return ""


@router.get("/entries")
def query_entry(db: Session = Depends(get_db)):
    return ""


@router.get("/matching")
def query_matching(db: Session = Depends(get_db)):
    return ""


@router.post("/match_making")
def make_match(req: MatchMakingRequest, db: Session = Depends(get_db)):
    m: domain.Match = match_making.make_match(db, req.to_model())
    return MatchMakingResponse.from_model(m.parties)


@router.post("/match_making_proto")
def make_match_proto(req: MatchMakingRequest, db: Session = Depends(get_db)) -> MatchMakingResponse:
    m: domain.Match = match_making.make_match(db, req.to_model())
    return MatchMakingResponse.from_model(m.parties)
