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

def load_data():
    connection = establish_connection()
    cursor = connection.cursor()


if __name__ == "__main__":
    connection = establish_connection()
    print(connection)
    connection.close()