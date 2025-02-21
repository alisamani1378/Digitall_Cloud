import os
import psycopg2

def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable '{name}' is not set or empty.")
    return value

DB_NAME = get_env_var("DB_NAME")
DB_USER = get_env_var("DB_USER")
DB_PASS = get_env_var("DB_PASS")
DB_HOST = get_env_var("DB_HOST")
DB_PORT = get_env_var("DB_PORT")

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
