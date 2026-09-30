"""
load.py

Loads the data into PostgreSQL database
"""
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def establish_connection():
    connection = psycopg.connect(dbname=os.getenv("DATABASE_NAME"), 
                                 host=os.getenv("DATABASE_HOST"), 
                                 port=os.getenv("DATABASE_PORT"), 
                                 user=os.getenv("DATABASE_USER"), 
                                 password=os.getenv("DATABASE_PASSWORD"))
    return connection

def load_data(df, user_id):
    connection = establish_connection()
    curr = connection.cursor()

    try:
        # Type lookup
        curr.execute("SELECT type_id, name FROM type")
        types = curr.fetchall()
        type_map = {}
        for type_id, type_name in types:
            type_map[type_name] = type_id

        # Category handling
        curr.execute("SELECT category_id, name FROM category WHERE user_id = %s", (user_id,))
        categories = curr.fetchall()
        category_map = {}
        for category_id, category_name in categories:
            category_map[category_name] = category_id
        csv_categories = df["Category"].unique()
        for category in csv_categories:
            if category not in category_map:
                curr.execute("INSERT INTO category (name, user_id) VALUES (%s, %s) RETURNING category_id", (category, user_id,))
                curr_category = curr.fetchone()
                category_map[category] = curr_category[0]

        # Transaction handling
        transactions = []
        transaction_df = df.select("Date", "Transaction Description", "Amount", "Category", "Type")
        rows = transaction_df.rows()
        for date, description, amount, category, type in rows:
            category_id = category_map[category]
            type_id = type_map[type]
            transactions.append((date, description, amount, user_id, category_id, type_id)) 
        curr.executemany("INSERT INTO transactions (date, description, amount, user_id, category_id, type_id) VALUES (%s, %s, %s, %s, %s, %s)", transactions)

        connection.commit()
        return True, None

    except psycopg.Error as error:
        connection.rollback()
        return False, error

    finally:
        curr.close()
        connection.close()

