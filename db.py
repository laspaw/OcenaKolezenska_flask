from flask import g
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
import os

load_dotenv()


class PGRepository:
    def __init__(self):
        self.connection = self.get_connection()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.create_tables()

    def get_connection(self):
        if 'connection' not in g:
            if os.getenv('DATABASE_URL', None) is None:
                g.connection = psycopg2.connect(host=os.getenv('DB_HOST', 'db'), dbname=os.getenv('DB_NAME', 'app_db'),
                                                user=os.getenv('DB_USER', 'sa'), password=os.getenv('DB_PASSWORD'))
            else:
                g.connection = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require'),
        return g.connection

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id serial primary key,
                email varchar(255) unique not null,
                password_hash varchar(255) not null,
                password_salt varchar(255) not null
                );
        """)
        self.connection.commit()


def close_connection(self):
    connection = g.pop('connection', None)
    if connection is not None:
        connection.close()


def init_app(app):
    # instrukcja wykonywana przy zamykaniu aplikacji
    app.teardown_appcontext(close_connection)
