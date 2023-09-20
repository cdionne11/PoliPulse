from flask import Flask, request, jsonify, render_template
from db.models import Filing, Contribution, Registrant, Client, Lobbyist
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from scripts.fetch_data import fetch_lobbyist_data, fetch_filing_data, fetch_contribution_data

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', active_page='home')


@app.route('/lobbyists', methods=['GET'])
def get_lobbyists():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    data = fetch_lobbyist_data(page=page, per_page=per_page)

    total_data = data['count']  # Updated line to use 'count' key

    print(data['results'])  # Add this line to print data and check if it's correct

    return render_template(
        'lobbyists.html',
        data=data['results'],  # Pass only the 'results' part of data to the template
        page=page,
        per_page=per_page,
        total_data=total_data,  # Updated line to pass total_data
        active_page='lobbyists'
    )


@app.route('/filings', methods=['GET'])
def get_filings():
    page = request.args.get('page', 1, type=int)
    filing_year = request.args.get('filing_year', 2023, type=int)
    per_page = 10
    data = fetch_filing_data(page=page, per_page=per_page, filing_year=filing_year)

    if data:
        total_data = data.get('count', 0)
        results = data.get('results', [])
    else:
        total_data = 0
        results = []

    total_pages = (total_data + per_page - 1) // per_page

    return render_template(
        'filings.html',
        data=results,
        page=page,
        per_page=per_page,
        total_data=total_data,
        total_pages=total_pages,
        active_page='filings'
    )


@app.route('/contributions', methods=['GET'])
def get_contributions():
    """Endpoint to retrieve data on contributions.

    Returns:
        json: A JSON object containing a list of contributions.
    """
    page = request.args.get('page', 1, type=int)
    filing_year = request.args.get('filing_year', 2023, type=int)
    per_page = 10
    data = fetch_contribution_data(page=page, per_page=per_page, filing_year=filing_year)  # Corrected the function name

    if data:
        total_data = data.get('count', 0)
        results = data.get('results', [])
    else:
        total_data = 0
        results = []

    total_pages = (total_data + per_page - 1) // per_page

    return render_template(
        'contributions.html',
        data=results,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_data=total_data,
        active_page='contributions'
    )


if __name__ == '__main__':
    app.run(debug=True)
