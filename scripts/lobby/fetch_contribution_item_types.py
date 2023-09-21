import requests
from db.models import ContributionItemTypes
import time
from db.session import SessionLocal

# Create a session for making API requests
session = requests.Session()


def fetch_contribution_type_data(max_pages=10):
    db = SessionLocal()
    try:
        page = 1
        all_data_downloaded = False  # Initialize a flag to False

        while max_pages is None or page <= max_pages:
            url = f"https://lda.senate.gov/api/v1/constants/contribution/itemtypes/?page={page}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            data = response.json()

            # Check if the response is a list of dictionaries
            if not isinstance(data, list):
                print("API response is not a list of dictionaries.")
                break

            # Iterate through the list of dictionaries
            for item_type_data in data:
                type_data = {
                    'value': item_type_data['value'],
                    'name': item_type_data['name']
                }

                # Check if the record already exists in the database
                existing_record = db.query(ContributionItemTypes).filter_by(value=type_data['value']).first()

                if not existing_record:
                    try:
                        contribution_record = ContributionItemTypes(**type_data)
                        db.add(contribution_record)  # Use 'add' to insert new records
                        print(f"Contribution item type added: {contribution_record}")  # Debug print
                    except Exception as e:
                        db.rollback()
                        print(f"Failed to add contribution item type: {e}")

            # Commit the changes to the database
            db.commit()

            # Check if there is another page
            if 'next' not in data:
                all_data_downloaded = True  # Set the flag to True when there's no more data
                break

            # Update the page number
            page += 1

            # Rate limiting with exponential backoff
            sleep_time = 4 * (2 ** (page - 2))  # Exponential backoff
            time.sleep(sleep_time)

        if all_data_downloaded:
            print("All data has been downloaded.")

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
    fetch_contribution_type_data(max_pages=100)  # Fetch data from the first 100 pages


if __name__ == "__main__":
    main()
