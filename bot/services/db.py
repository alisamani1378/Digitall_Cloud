import os
import psycopg2

DB_NAME = os.getenv("DB_NAME", "shopdb")
DB_USER = os.getenv("DB_USER", "shopuser")
DB_PASS = os.getenv("DB_PASS", "supersecret")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            username VARCHAR(100),
            balance NUMERIC(10,2) DEFAULT 0
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_user_to_db(telegram_id, first_name, last_name, username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (telegram_id, first_name, last_name, username)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (telegram_id)
        DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            username = EXCLUDED.username;
    """, (telegram_id, first_name, last_name, username))

    conn.commit()
    cur.close()
    conn.close()
