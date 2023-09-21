import requests
from db.models import Client
import time
from datetime import datetime
from db.session import SessionLocal

# Create a session for making API requests
session = requests.Session()


def fetch_client_data(page=1, per_page=1000, max_pages=None, filing_year=2023):
    db = SessionLocal()
    try:
        while max_pages is None or page <= max_pages:
            url = f"https://lda.senate.gov/api/v1/clients/?page={page}&per_page={per_page}&filing_year={filing_year}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            count = data['count']
            next_page = data['next']
            previous = data['previous']

            # Access the 'results' list and iterate through it
            for result in data['results']:
                client_data = {
                    'id': result['id'],
                    'client_id': result['client_id'],
                    'url': result['url'],
                    'name': result['name'],
                    'general_description': result['general_description'],
                    'client_government_entity': result['client_government_entity'],
                    'state': result['state'],
                    'state_display': result['state_display'],
                    'country': result['country'],
                    'country_display': result['country_display'],
                    'ppb_state': result['ppb_state'],
                    'ppb_state_display': result['ppb_state_display'],
                    'ppb_country': result['ppb_country'],
                    'ppb_country_display': result['ppb_country_display'],
                    'effective_date': datetime.strptime(result['effective_date'], '%Y-%m-%d')  # Convert to date object
                }

                registrant = result.get('registrant')

                if isinstance(registrant, dict):
                    client_data['registrant_id'] = registrant.get('id')

                try:
                    client_record = Client(**client_data)
                    db.merge(client_record)
                    print(f"Client added or updated: {client_record}")  # Debug print
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add or update registrant: {e}")

            # Commit the changes to the database
            db.commit()

            if not next_page:
                break

            page += 1

            # Rate limiting with exponential backoff
            sleep_time = 4 * (2 ** (page - 2))  # Exponential backoff
            time.sleep(sleep_time)

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
        return None  # Ensure that a value is returned even if an error occurs


def main():
    fetch_client_data(max_pages=100)  # Fetch data from the first 100 pages


if __name__ == "__main__":
    main()
