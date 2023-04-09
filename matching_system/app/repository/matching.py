from app.domain.matching import Match, AMatchRepository
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

class MatchRepository(AMatchRepository):
    def __init__(self, db: Session) -> None:
        self.store = db
    
    def save(self, payload: Match) -> Match:
        return "TODO"
