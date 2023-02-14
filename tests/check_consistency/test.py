import datetime
import os
from pathlib import Path
import sqlite3

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor


load_dotenv()

base_path = Path(__file__).resolve().parent.parent.parent
sqlite_db = (base_path / 'sqlite_to_postgres/db.sqlite')
tables = ['genre', 'person', 'film_work', 'genre_film_work', 'person_film_work']
postgres_dsn = {
    'dbname': 'movies_database',
    'user': 'postgres',
    'password': os.environ.get('DB_PASSWORD'),
    'host': '127.0.0.1',
    'port': 5432,
    'options': '-c search_path=content',
}


class SQLiteConnection:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, ex_type, ex_val, ex_tb):
        if ex_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


class PostgresConnection:
    def __init__(self, dbname, user, password, host, port, options):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.options = options

    def __enter__(self):
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                     host=self.host, port=self.port, options=self.options)
        return self.conn

    def __exit__(self, ex_type, ex_val, ex_tb):
        if ex_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


def test_data_integrity():
    """Check the integrity between SQLite DB and PostgreSQL DB.

    Show if the number of records in each of the corresponding tables is the same.
    """

    with SQLiteConnection(sqlite_db) as sqlite_conn:
        with PostgresConnection(**postgres_dsn) as postgres_conn:
            for table in tables:
                sqlite_curs = sqlite_conn.cursor()
                postgres_curs = postgres_conn.cursor()

                sqlite_curs.execute(f'SELECT COUNT(*) FROM {table}')
                postgres_curs.execute(f'SELECT COUNT(*) FROM {table}')

                sqlite_count = sqlite_curs.fetchone()[0]
                postgres_count = postgres_curs.fetchone()[0]

                assert sqlite_count == postgres_count, (
                    f'Mismatch between SQLite and PostgreSQL table {table} detected.'
                )


def test_data_content():
    """Check the content in both SQLite DB and PostgreSQL DB.

    Show if the content of each record in both DB is the same.
    """

    with SQLiteConnection(sqlite_db) as sqlite_conn:
        with PostgresConnection(**postgres_dsn) as postgres_conn:
            for table in tables:
                sqlite_curs = sqlite_conn.cursor()
                postgres_curs = postgres_conn.cursor(cursor_factory=DictCursor)

                sqlite_curs.execute(f'SELECT * FROM {table}')
                postgres_curs.execute(f'SELECT * FROM {table}')

                sqlite_select = sqlite_curs.fetchall()
                postgres_select = postgres_curs.fetchall()

                for i in range(len(sqlite_select)):
                    sqlite_dict = dict(sqlite_select[i])
                    for key, value in sqlite_dict.items():
                        if key.find('_at') != -1:
                            new_value = str(value) + '00'
                            dt_value = datetime.datetime.strptime(
                                new_value, '%Y-%m-%d %H:%M:%S.%f%z'
                            )
                            sqlite_dict.update({key: dt_value})
                    assert list(sqlite_dict.values()) == postgres_select[i], (
                        f'Mismatch between SQLite and PostgreSQL in table "{table}" detected.'
                    )
