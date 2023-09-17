import os
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
from db.models import User  # Make sure the path is correct
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, 'db')
db_path = os.path.join(DATABASE_DIR, 'polipulse.db')
engine = create_engine('sqlite:///' + db_path)
SessionLocal = sessionmaker(bind=engine)

def authenticate():
    """
    Authenticates a user with the Senate API using the credentials stored in environment variables.

    Returns:
        tuple: A tuple containing a requests Session object and the authentication token.
    """

    # Define the authentication credentials
    username = os.getenv("SENATE_USERNAME")
    password = os.getenv("SENATE_PASSWORD")

    if not username or not password:
        logging.error("Please set SENATE_USERNAME and SENATE_PASSWORD environment variables.")
        exit(1)

    # Create a session for making API requests
    session = requests.Session()

    # Define the Login API endpoint URL
    login_url = 'https://lda.senate.gov/api/auth/login/'

    # Define the request payload with your credentials
    payload = {
        'username': username,
        'password': password
    }

    # Create a new session for database interaction
    db = SessionLocal()

    try:
        # Send the POST request to log in
        login_response = session.post(login_url, json=payload)
        login_response.raise_for_status()

        # Get the authentication token from the response
        authentication_token = login_response.json().get('key')
        logging.info(f'Authentication successful. Token: {authentication_token}')

        # Check if a user entry already exists
        user = db.query(User).first()

        if user:
            # Update the existing user token
            user.token = authentication_token
        else:
            # Create a new user entry
            new_user = User(token=authentication_token)
            db.add(new_user)

        # Commit the changes to the database
        db.commit()

        return session, authentication_token
    except RequestException as e:
        logging.error(f'Authentication failed. Error: {e}')
        exit(1)
    finally:
        # Close the database session
        db.close()
