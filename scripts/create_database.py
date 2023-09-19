import logging
from db.models import (
    Base,
    User,
    Filing,
    Contribution,
    Registrant,
    Client,
    Lobbyist,
    ContributionItemTypes,
    Countries,
    LobbyActivityIssues,
    States,
    FilingTypes,
    LobbistSuffixes,
    LobbistPrefixes
)
from db.session import engine

# Configure logging
logging.basicConfig(level=logging.INFO)


def ensure_database_exists():
    """
    Ensures the database and required tables exist. If the tables do not exist, it creates them.

    Raises:
        Exception: Any exception that occurs during table creation.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Tables created successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    ensure_database_exists()
