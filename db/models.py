from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Example date and time string from API response
date_time_str = "2023-09-21T14:30:00Z"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)


class Lobbyist(Base):
    __tablename__ = 'lobbyists'
    id = Column(Integer, primary_key=True, index=True)
    prefix = Column(String)
    prefix_display = Column(String)
    first_name = Column(String)
    nickname = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    suffix = Column(String)
    suffix_display = Column(String)
    registrant_id = Column(Integer, ForeignKey('registrants.id'), nullable=True)  # ForeignKey to the Registrant class
    registrant = relationship('Registrant', back_populates='lobbyists')  # defining the relationship


class Filing(Base):
    __tablename__ = 'filings'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    filing_uuid = Column(String, unique=True, index=True)
    filing_type = Column(String)
    filing_type_display = Column(String)
    filing_year = Column(Integer)
    filing_period = Column(String)
    filing_period_display = Column(String)
    filing_document_url = Column(String)
    filing_document_content_type = Column(String)
    income = Column(Float)  # Assuming income can be represented as a floating-point number
    expenses = Column(Float)  # Assuming expenses can be represented as a floating-point number
    expenses_method = Column(String)
    expenses_method_display = Column(String)
    posted_by_name = Column(String)
    dt_posted = Column(DateTime)
    termination_date = Column(Date)  # Assuming termination_date should be a date type
    registrant_country = Column(String)
    registrant_ppb_country = Column(String)
    registrant_address_1 = Column(String)
    registrant_address_2 = Column(String)
    registrant_different_address = Column(String)
    registrant_city = Column(String)
    registrant_state = Column(String)
    registrant_zip = Column(String)
    # lobbying_activities = Column(String)
    general_issue_code = Column(String)
    # general_issue_code_display = Column(String)
    # description = Column(String)
    # foreign_entity_issues = Column(String)
    registrant_id = Column(Integer, ForeignKey('registrants.id'))  # Create a foreign key to a Registrant table
    client_id = Column(Integer, ForeignKey('clients.id'))  # Create a foreign key to a Client table

    # Relationships to other tables (assuming these tables exist in your database)
    registrant = relationship('Registrant', back_populates='filings')
    client = relationship('Client', back_populates='filings')


class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True, index=True)
    donor_name = Column(String, index=True)
    amount = Column(Integer)


class Registrant(Base):
    __tablename__ = 'registrants'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    name = Column(String, index=True)
    description = Column(String)
    address_1 = Column(String)
    address_2 = Column(String)
    address_3 = Column(String)
    address_4 = Column(String)
    city = Column(String)
    state = Column(String)
    state_display = Column(String)
    zip = Column(Integer)
    country = Column(String)
    country_display = Column(String)
    ppb_country = Column(String)
    ppb_country_display = Column(String)
    contact_name = Column(String)
    contact_telephone = Column(String)
    dt_updated = Column(String)

    # TODO: Add foreign key to house_registrant
    house_registrant_id = Column(String)

    lobbyists = relationship('Lobbyist', back_populates='registrant')
    filings = relationship('Filing', back_populates='registrant')



class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, unique=True, index=True)
    url = Column(String)
    name = Column(String, index=True)
    general_description = Column(String)
    client_government_entity = Column(String)
    client_self_select = Column(Boolean)
    state = Column(String)
    state_display = Column(String)
    country = Column(String)
    country_display = Column(String)
    ppb_state = Column(String)
    ppb_state_display = Column(String)
    ppb_country = Column(String)
    ppb_country_display = Column(String)
    effective_date = Column(Date)  # assuming date format is 'YYYY-MM-DD'

    registrant_id = Column(Integer, ForeignKey('registrants.id'), nullable=True)
    registrant = relationship('Registrant', back_populates='clients')
    filings = relationship('Filing', back_populates='client')


Registrant.clients = relationship('Client', back_populates='registrant')


class FilingTypes(Base):
    __tablename__ = 'filing_type'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(100), index=True)
    name = Column(String, index=True)


class LobbyActivityIssues(Base):
    __tablename__ = 'lobby_activity_issues'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)


class GovernmentEntities(Base):
    __tablename__ = 'government_entities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)


class States(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)


class LobbistPrefixes(Base):
    __tablename__ = 'lobbist_prefixes'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)


class LobbistSuffixes(Base):
    __tablename__ = 'lobbist_suffixes'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)


class ContributionItemTypes(Base):
    __tablename__ = 'contribution_item_types'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, index=True)
    name = Column(String, index=True)