from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)


class Lobbyist(Base):
    __tablename__ = 'lobbyists'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    affiliations = Column(String)


class Filing(Base):
    __tablename__ = 'filings'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_filed = Column(DateTime)


class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True, index=True)
    donor_name = Column(String, index=True)
    amount = Column(Integer)


class Registrant(Base):
    __tablename__ = 'registrants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class FilingTypes(Base):
    __tablename__ = 'filing_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class LobbyActivityIssues(Base):
    __tablename__ = 'lobby_activity_issues'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class GovernmentEntities(Base):
    __tablename__ = 'government_entities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class States(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class LobbistPrefixes(Base):
    __tablename__ = 'lobbist_prefixes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class LobbistSuffixes(Base):
    __tablename__ = 'lobbist_suffixes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))


class ContributionItemTypes(Base):
    __tablename__ = 'contribution_item_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    industry = Column(String(100))