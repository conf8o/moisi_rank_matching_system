from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import app.use_case.match_making as match_making
import app.domain.matching as domain
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
    players: list[Player]

    def to_model(self) -> domain.Entry:
        return domain.Entry([p.to_model() for p in self.players])

class Party(BaseModel):
    players: list[Player]

    @staticmethod
    def from_model(party: domain.Party) -> 'Party':
        return Party(players=[Player.from_model(p) for p in party.players])


class MatchMakingRequest(BaseModel):
    entries: list[Entry]

    def to_model(self) -> list[domain.Entry]:
        return [e.to_model() for e in self.entries]


class MatchMakingResponse(BaseModel):
    parties: list[Party]

    @staticmethod
    def from_model(parties: list[domain.Party]) -> 'MatchMakingResponse':
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
    return str(db)


@router.post("/match_making_proto")
def make_match_proto(req: MatchMakingRequest) -> list[Player]:
    m: domain.Match = match_making.make_match(match_making.MockMatchRepository(None), req.to_model())
    return MatchMakingResponse.from_model(m.parties)
