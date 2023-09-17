from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)


class Filing(Base):
    __tablename__ = 'filings'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_filed = Column(DateTime)
    # ... add more fields based on the data returned by the filings endpoint


class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True, index=True)
    donor_name = Column(String, index=True)
    amount = Column(Integer)
    # ... add more fields based on the data returned by the contributions endpoint


class Registrant(Base):
    __tablename__ = 'registrants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    # ... add more fields based on the data returned by the registrants endpoint


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))  # And here
    # ... add more fields based on the data returned by the clients endpoint


class Lobbyist(Base):
    __tablename__ = 'lobbyists'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    affiliations = Column(String)
    # ... add more fields based on the data returned by the lobbyists endpoint

class Filing_Types(Base):
    __tablename__ = 'filing_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))  # And here

class Lobby_Activity_Issues(Base):
    __tablename__ = 'lobby_activity_issues'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))

class Government_Entities(Base):
    __tablename__ = 'government_entities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))

class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))

class States(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))

class Lobbist_Prefixes(Base):
    __tablename__ = 'lobbist_prefixes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))

class Lobbist_Suffixes(Base):
    __tablename__ = 'lobbist_suffixes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))

class Contribution_ItemTypes(Base):
    __tablename__ = 'contribution_item_types'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Added length constraint here
    industry = Column(String(100))