from dotenv import load_dotenv

from scripts import create_database
from scripts.auth import authenticate

# Import the Flask app object
from api.app import app


def main():
    # Load environment variables
    load_dotenv()

    # Ensure the database exists
    create_database.ensure_database_exists()

    # Authenticate the user for API access
    authenticate()

    # Start the Flask app
    app.run(debug=True)


if __name__ == "__main__":
    main()
