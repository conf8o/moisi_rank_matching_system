import domain.matching as domain
from sqlalchemy.orm import Session
from sqlalchemy import Column, ForeignKey, DateTime, String, Integer, insert
from database import Base, ID
from datetime import datetime
from collections import defaultdict

class Match(Base):
    id = Column("id", ID, primary_key=True)
    created_at = Column("created_at", DateTime, default=datetime.now, nullable=False)
    closed_at = Column("closed_at", DateTime)

    __tablename__ = "matches"


class Party(Base):
    id = Column("id", ID, primary_key=True)
    match_id = Column("match_id", Integer, ForeignKey("matches.id", onupdate="CASCADE", ondelete="CASCADE"))

    __tablename__ = "parties"


class Entry(Base):
    id = Column("id", ID, primary_key=True)
    created_at = Column("created_at", DateTime, default=datetime.now, nullable=False)
    closed_at = Column("closed_at", DateTime)

    __tablename__ = "entries"


class Player(Base):
    id = Column("id", ID, primary_key=True)
    name = Column("name", String(255), nullable=False)
    point = Column("point", Integer, nullable=False)

    __tablename__ = "players"


class PartyPlayer(Base):
    party_id = Column("party_id", ID, ForeignKey("parties.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    player_id = Column("player_id", ID, ForeignKey("players.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    __tablename__ = "party_players"


class EntryPlayer(Base):
    entry_id = Column("entry_id", ID, ForeignKey("entries.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    player_id = Column("player_id", ID, ForeignKey("players.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

    __tablename__ = "entry_players"


class MatchRepository(domain.AMatchRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def find_by_id(self, id: ID) -> domain.Match:
        m = self.db.query(Match).filter(Match.id==id).first()
        parties = self.db.query(Party).filter(Party.match_id==id).all()
        players = self.db.query(PartyPlayer.party_id, Player) \
            .outerjoin(PartyPlayer, Player.id==PartyPlayer.player_id) \
            .filter(PartyPlayer.party_id.in_(p.id for p in parties)) \
            .all()
        
        players_by_party_id = defaultdict(list)
        for party_id, player in players:
            players_by_party_id[party_id].append(domain.Player(player.id, player.name, player.point))

        parties = [domain.Party(p.id, players_by_party_id[p.id]) for p in parties]
        return domain.Match(id, parties)
            
    def save(self, payload: domain.Match) -> domain.Match:
        match_id = payload.id

        domain_parties: list[domain.Party] = payload.parties

        match = Match()
        match.id = match_id
        self.db.add(match)


        parties = []
        players = []
        party_players = []
        for domain_party in domain_parties:
            party = Party()
            party.id = domain_party.id # モデルにidを追加する
            party.match_id = match_id
            parties.append(party)

            domain_players = domain_party.players
            for domain_player in domain_players:
                player = Player()
                player.id = domain_player.id
                player.name = domain_player.name
                player.point = domain_player.point
                players.append(player)

                party_player = PartyPlayer()
                party_player.party_id = party.id
                party_player.player_id = domain_player.id
                party_players.append(party_player)

        self.db.add_all(parties)
        self.db.add_all(players)
        self.db.add_all(party_players)
        self.db.commit()

        return self.find_by_id(match_id)
