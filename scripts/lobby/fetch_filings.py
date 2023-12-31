import requests
from db.models import Filing
import time
from datetime import datetime
from db.session import SessionLocal

# Create a session for making API requests
session = requests.Session()


def fetch_filing_data(page=1, per_page=1000, max_pages=None, filing_year=2023):
    db = SessionLocal()
    try:
        while max_pages is None or page <= max_pages:
            url = f"https://lda.senate.gov/api/v1/filings/?page={page}&per_page={per_page}&filing_year={filing_year}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            count = data['count']
            next_page = data['next']
            previous = data['previous']

            # Access the 'results' list and iterate through it
            for result in data['results']:
                filing_data = {
                    'url': result['url'],
                    'filing_uuid': result['filing_uuid'],
                    'filing_type': result['filing_type'],
                    'filing_type_display': result['filing_type_display'],
                    'filing_year': result['filing_year'],
                    'filing_period': result['filing_period'],
                    'filing_period_display': result['filing_period_display'],
                    'filing_document_url': result['filing_document_url'],
                    'filing_document_content_type': result['filing_document_content_type'],
                    'income': result['income'],
                    'expenses': result['expenses'],
                    'expenses_method': result['expenses_method'],
                    'expenses_method_display': result['expenses_method_display'],
                    'posted_by_name': result['posted_by_name'],
                    'dt_posted': datetime.strptime(result['dt_posted'], '%Y-%m-%dT%H:%M:%S%z'),
                    'termination_date': None,
                    'registrant_country': result['registrant_country'],
                    'registrant_ppb_country': result['registrant_ppb_country'],
                    'registrant_address_1': result['registrant_address_1'],
                    'registrant_address_2': result['registrant_address_2'],
                    'registrant_different_address': result['registrant_different_address'],
                    'registrant_city': result['registrant_city'],
                    'registrant_state': result['registrant_state'],
                    'registrant_zip': result['registrant_zip']
                }

                registrant = result.get('registrant')
                client = result.get('client')

                if result['termination_date']:
                    filing_data['termination_date'] = datetime.strptime(result['termination_date'], '%Y-%m-%d').date()

                if isinstance(registrant, dict):
                    filing_data['registrant_id'] = registrant.get('id')

                if isinstance(client, dict):
                    filing_data['client_id'] = client.get('id')

                # Check if a record with the same filing_uuid already exists in the database
                existing_filing = db.query(Filing).filter_by(filing_uuid=result['filing_uuid']).first()

                if existing_filing:
                    # Update the existing record
                    for key, value in filing_data.items():
                        setattr(existing_filing, key, value)
                    print(f"Filing updated: {existing_filing}")  # Debug print
                else:
                    # Insert a new record
                    try:
                        filing_record = Filing(**filing_data)
                        db.add(filing_record)
                        print(f"Filing added: {filing_record}")  # Debug print
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
    fetch_filing_data(max_pages=100)  # Fetch data from the first 100 pages


if __name__ == "__main__":
    main()
