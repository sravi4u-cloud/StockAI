import sqlite3
from pathlib import Path

# Get the absolute path of the StockAI project folder

BASE_DIR = Path(__file__).resolve().parent.parent

# Create the db folder inside StockAI

DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)

# Full path to the SQLite database

DB_PATH = DB_DIR / "stock.db"

def get_connection():
 return sqlite3.connect(DB_PATH)
