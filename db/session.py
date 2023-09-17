from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

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
