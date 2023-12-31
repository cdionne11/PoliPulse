import requests
from db.models import Registrant
import time
from db.session import SessionLocal

# Create a session for making API requests
session = requests.Session()


def fetch_registrant_data(page=1, per_page=1000, max_pages=None):
    db = SessionLocal()
    try:
        while max_pages is None or page <= max_pages:
            url = f"https://lda.senate.gov/api/v1/registrants/?page={page}&per_page={per_page}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            count = data['count']
            next_page = data['next']
            previous = data['previous']

            # Access the 'results' list and iterate through it
            for result in data['results']:
                registrant_data = {
                    'id': result['id'],
                    'url': result['url'],
                    'house_registrant_id': result['house_registrant_id'],
                    'name': result['name'],
                    'description': result['description'],
                    'address_1': result['address_1'],
                    'address_2': result['address_2'],
                    'address_3': result['address_3'],
                    'address_4': result['address_4'],
                    'city': result['city'],
                    'state': result['state'],
                    'state_display': result['state_display'],
                    'zip': result['zip'],
                    'country': result['country'],
                    'country_display': result['country_display'],
                    'ppb_country': result['ppb_country'],
                    'ppb_country_display': result['ppb_country_display'],
                    'contact_name': result['contact_name'],
                    'contact_telephone': result['contact_telephone'],
                    'dt_updated': result['dt_updated']
                }

                registrant = result.get('registrant')

                if isinstance(registrant, dict):
                    registrant_data['registrant_id'] = registrant.get('id')

                # Attempt to merge the registrant data into the database
                try:
                    registrant_record = Registrant(**registrant_data)
                    db.merge(registrant_record)
                    print(f"Registrant added or updated: {registrant_record}")  # Debug print
                except Exception as e:
                    db.rollback()  # Rollback any changes if an error occurs
                    print(f"Failed to add or update registrant: {e}")

            # Commit the changes to the database
            db.commit()

            if not next_page:
                break  # No more pages to fetch

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
    fetch_registrant_data(max_pages=100)  # Fetch data from the first 100 pages


if __name__ == "__main__":
    main()
