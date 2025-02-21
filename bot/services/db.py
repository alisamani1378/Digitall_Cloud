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

    # جدول users (قبلاً موجود بود)
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

    # جدول products
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            price NUMERIC(10,2) NOT NULL DEFAULT 0
        );
    """)

    # جدول orders
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_user_to_db(telegram_id, first_name, last_name, username):
    """
    درج یا بروزرسانی اطلاعات کاربر در جدول users براساس telegram_id.
    """
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

def add_product(title, price):
    """
    درج محصول جدید در جدول products.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (title, price)
        VALUES (%s, %s)
        RETURNING id;
    """, (title, price))
    product_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return product_id

def get_all_products():
    """
    فهرست همه محصولات را برمی‌گرداند (id, title, price).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, price FROM products ORDER BY id;")
    products = cur.fetchall()  # list of tuples [(id, title, price), ...]
    cur.close()
    conn.close()
    return products

def get_product_by_id(product_id):
    """
    یک محصول را براساس ID برمی‌گرداند (id, title, price).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, price FROM products WHERE id = %s;", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    return product
def create_order(user_id, product_id):
    """
    ایجاد سفارش جدید در وضعیت 'pending'.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO orders (user_id, product_id)
        VALUES (%s, %s)
        RETURNING id;
    """, (user_id, product_id))
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return order_id

def get_order_by_id(order_id):
    """
    بازیابی مشخصات یک سفارش براساس ID.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, product_id, created_at, status FROM orders WHERE id = %s;", (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()
    return order

def update_order_status(order_id, new_status):
    """
    تغییر وضعیت سفارش (مثلاً از 'pending' به 'paid').
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE orders
        SET status = %s
        WHERE id = %s;
    """, (new_status, order_id))
    conn.commit()
    cur.close()
    conn.close()
