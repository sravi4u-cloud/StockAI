import sqlite3
import bcrypt
from datetime import datetime

DB_PATH = "database/stockai.db"

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Hash password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        cursor.execute("""
        INSERT INTO users (username, password_hash, created_at)
        VALUES (?, ?, ?)
        """, (username, password_hash.decode("utf-8"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        print("User created successfully!")

    except sqlite3.IntegrityError:
        print("Username already exists!")

    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_hash = result[0].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

    return False