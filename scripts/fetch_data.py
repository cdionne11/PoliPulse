import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from db.models import Filing, Contribution, Registrant, Client, Lobbyist, FilingTypes, LobbyActivityIssues, \
    GovernmentEntities, Countries, States, LobbistPrefixes, LobbistSuffixes, ContributionItemTypes

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Create a session for making API requests
session = requests.Session()

API_ENDPOINTS = {
    "filings": "https://lda.senate.gov/api/v1/filings/?format=api",
    "contributions": "https://lda.senate.gov/api/v1/contributions/?format=api",
    "registrants": "https://lda.senate.gov/api/v1/registrants/?format=api",
    "clients": "https://lda.senate.gov/api/v1/clients/?format=api",
    "lobbyists": "https://lda.senate.gov/api/v1/lobbyists/?format=api",
    "filing_types": "https://lda.senate.gov/api/v1/constants/filing/filingtypes/?format=api",
    "lobbying_activity_issues": "https://lda.senate.gov/api/v1/constants/filing/lobbyingactivityissues/?format=api",
    "government_entities": "https://lda.senate.gov/api/v1/constants/filing/governmententities/?format=api",
    "countries": "https://lda.senate.gov/api/v1/constants/general/countries/?format=api",
    "states": "https://lda.senate.gov/api/v1/constants/general/states/?format=api",
    "constants/lobbyist/prefixes": "https://lda.senate.gov/api/v1/constants/lobbyist/prefixes/?format=api",
    "constants/lobbyist/suffixes": "https://lda.senate.gov/api/v1/constants/lobbyist/suffixes/?format=api",
    "constants/contribution/itemtypes": "https://lda.senate.gov/api/v1/constants/contribution/itemtypes/?format=api"
}


def fetch_data(endpoint, model):
    url = API_ENDPOINTS.get(endpoint)

    if not url:
        print(f"Invalid endpoint: {endpoint}")
        return

    try:
        response = session.get(url, params={"format": "api"})
        response.raise_for_status()
        data = response.json()

        for item in data:
            new_record = model(**item)  # Assuming field names match exactly
            db.add(new_record)

        db.commit()
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


def fetch_lobbyist_data(page=1, per_page=10):
    url = f"https://lda.senate.gov/api/v1/lobbyists/?page={page}&per_page={per_page}"
    response = requests.get(url)
    data = response.json()
    return data


def fetch_filing_data(page=1, per_page=10, filing_year=2023):
    url = f"https://lda.senate.gov/api/v1/filings/?filing_year={filing_year}&page={page}&page_size={per_page}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
        return None



def main():
    fetch_data('filings', Filing)
    fetch_data('contributions', Contribution)
    fetch_data('registrants', Registrant)
    fetch_data('clients', Client)
    fetch_data('lobbyists', Lobbyist)
    fetch_data('filing_types', FilingTypes)
    # fetch_data('lobby_activity_issues', LobbyActivityIssues)
    # fetch_data('government_entities', GovernmentEntities)
    # fetch_data('countries', Countries)
    # fetch_data('states', States)
    # fetch_data('lobbiest_prefixes', LobbistPrefixes)
    # fetch_data('lobbiest_suffixes', LobbistSuffixes)
    # fetch_data('contribution_item_types', ContributionItemTypes)


if __name__ == "__main__":
    main()
