import domain.matching as domain
from sqlalchemy.orm import Session
from sqlalchemy import Column, ForeignKey, DATETIME, String, Integer, insert
from database import Base
from datetime import datetime

class Match(Base):
    id = Column("id", Integer, primary_key=True)
    created_at = Column("created_at", DATETIME, default=datetime.now, nullable=False)
    closed_at = Column("closed_at", DATETIME)

    __tablename__ = "matches"


class Party(Base):
    id = Column("id", Integer, primary_key=True)
    match_id = Column("match_id", Integer, ForeignKey("matches.id", onupdate="CASCADE", ondelete="CASCADE"))

    __tablename__ = "parties"


class Entry(Base):
    id = Column("id", Integer, primary_key=True)
    created_at = Column("created_at", DATETIME, default=datetime.now, nullable=False)
    closed_at = Column("closed_at", DATETIME)

    __tablename__ = "entries"


class Player(Base):
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(255), nullable=False)
    point = Column("point", Integer, nullable=False)

    __tablename__ = "players"


class PartyPlayer(Base):
    party_id = Column("party_id", Integer, primary_key=True)
    player_id = Column("player_id", Integer, primary_key=True)

    __tablename__ = "party_players"


class EntryPlayer(Base):
    entry_id = Column("party_id", Integer, primary_key=True)
    player_id = Column("player_id", Integer, primary_key=True)

    __tablename__ = "entry_players"


class MatchRepository(domain.AMatchRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def save(self, payload: domain.Match) -> domain.Match:
        match_id = payload.id
        domain_parties: list[domain.Party] = payload.parties

        match = Match()
        match.id = match_id
        self.db.add(match)


        parties = []
        party_players = []
        for domain_party in domain_parties:
            party = Party()
            party.id = domain_party.id # モデルにidを追加する
            party.match_id = match_id
            parties.append(party)

            domain_players = domain_party.players
            for domain_player in domain_players:
                party_player = PartyPlayer()
                party_player.party_id = party.id
                party_player.player_id = domain_player.id
                party_players.append(party_player)

        self.db.add_all(parties)
        self.db.add_all(party_players)


        return ""
