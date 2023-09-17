from flask import Flask, request, jsonify, render_template
from db.models import Filing, Contribution, Registrant, Client, Lobbyist
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from scripts.fetch_data import fetch_lobbyist_data

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
    """Endpoint to retrieve data on filings.

    Returns:
        json: A JSON object containing a list of filings.
    """
    session = SessionLocal()
    try:
        filings = session.query(Filing).all()
        return jsonify([filing.to_dict() for filing in filings])
    finally:
        session.close()


@app.route('/contributions', methods=['GET'])
def get_contributions():
    """Endpoint to retrieve data on contributions.

    Returns:
        json: A JSON object containing a list of contributions.
    """
    session = SessionLocal()
    try:
        contributions = session.query(Contribution).all()
        return jsonify([contribution.to_dict() for contribution in contributions])
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True)
