import requests
from db.models import Contribution
import time
from db.session import SessionLocal

# Create a session for making API requests
session = requests.Session()


def fetch_contribution_data(page=1, max_pages=10, page_size=10, filing_year=2023):
    db = SessionLocal()
    try:
        page = 1
        all_data_downloaded = False  # Initialize a flag to False

        while max_pages is None or page <= max_pages:
            url = f"https://lda.senate.gov/api/v1/contributions/?page={page}&page_size={page_size}&filing_year={filing_year}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            count = data['count']
            next_page = data['next']
            previous = data['previous']

            # Access the 'results' list and iterate through it
            for result in data['results']:
                contribution_data = {
                    'url': result['url'],
                    'filing_uuid': result['filing_uuid'],
                    'filing_type': result['filing_type'],
                    'filing_type_display': result['filing_type_display'],
                    'filing_year': result['filing_year'],
                    'filing_period': result['filing_period'],
                    'filing_period_display': result['filing_period_display'],
                    'filing_document_url': result['filing_document_url'],
                    'filing_document_content_type': result['filing_document_content_type'],
                    'filer_type': result['filer_type'],
                    'filer_type_display': result['filer_type_display'],
                    'dt_posted': result['dt_posted'],
                    'contact_name': result['contact_name'],
                    'comments': result['comments'],
                    'address_1': result['address_1'],
                    'address_2': result['address_2'],
                    'city': result['city'],
                    'state': result['state'],
                    'state_display': result['state_display'],
                    'zip': result['zip'],
                    'country': result['country'],
                    'country_display': result['country_display']
                }

                registrant = result.get('registrant')

                if isinstance(registrant, dict):
                    contribution_data['registrant_id'] = registrant.get('id')

                # Check if a record with the same filing_uuid already exists in the database
                existing_filing = db.query(Contribution).filter_by(filing_uuid=result['filing_uuid']).first()

                if existing_filing:
                    # Update the existing record
                    for key, value in contribution_data.items():
                        setattr(existing_filing, key, value)
                    print(f"Contributions updated: {existing_filing}")  # Debug print
                else:
                    # Insert a new record
                    try:
                        contribution_record = Contribution(**contribution_data)
                        db.add(contribution_record)
                        print(f"Contributions added: {contribution_record}")  # Debug print
                    except Exception as e:
                        db.rollback()
                        print(f"Failed to add filing: {e}")

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


def main():
    fetch_contribution_data(max_pages=100)  # Fetch data from the first 100 pages


if __name__ == "__main__":
    main()
