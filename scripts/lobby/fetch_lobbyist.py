import os
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Lobbyist
import time  # Import the time module for rate limiting

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

db_path = os.path.join(DATABASE_DIR, 'polipulse.db')

if not os.path.isfile(db_path):
    open(db_path, 'w').close()

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Create a session for making API requests
session = requests.Session()


def fetch_lobbyist_data(page=1, per_page=1000, max_pages=None):
    try:
        while max_pages is None or page <= max_pages:
            url = f"https://lda.senate.gov/api/v1/lobbyists/?page={page}&per_page={per_page}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            count = data['count']
            next_page = data['next']
            previous = data['previous']

            # Access the 'results' list and iterate through it
            for result in data['results']:
                lobbyist_data = {
                    'id': result['id'],
                    'prefix': result['prefix'],
                    'prefix_display': result['prefix_display'],
                    'first_name': result['first_name'],
                    'nickname': result['nickname'],
                    'middle_name': result['middle_name'],
                    'last_name': result['last_name'],
                    'suffix': result['suffix'],
                    'suffix_display': result['suffix_display']
                }

                registrant = result.get('registrant')

                if isinstance(registrant, dict):
                    lobbyist_data['registrant_id'] = registrant.get('id')

                # Attempt to merge the lobbyist data into the database
                try:
                    lobbyist = Lobbyist(**lobbyist_data)
                    db.merge(lobbyist)
                    print(f"Lobbyist added or updated: {lobbyist}")  # Debug print
                except Exception as e:
                    db.rollback()  # Rollback any changes if an error occurs
                    print(f"Failed to add or update lobbyist: {e}")

            # Commit the changes to the database
            db.commit()

            if not next_page:
                break  # No more pages to fetch

            page += 1

            # Rate limiting: Sleep for a few seconds between requests
            time.sleep(4)  # Sleep for 2 seconds between requests

        return data
    except requests.exceptions.RequestException as e:
        # If there is any issue with the request (like network issues, timeout, etc.), this block will be executed
        print(f"Failed to fetch data: {e}")
        return None
    except ValueError:
        # If the response cannot be decoded as JSON, this block will be executed
        print("Failed to decode JSON from response")
        return None
    except Exception as e:
        # Handle any other exceptions here
        print(f"An error occurred: {e}")


def main():
    fetch_lobbyist_data(max_pages=100)  # Fetch data from the first 100 pages


if __name__ == "__main__":
    main()
