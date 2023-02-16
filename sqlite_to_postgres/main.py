import os
import sqlite3
from typing import Type, Union

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection

from data_extractor import SQLiteExtractor
from data_loader import load_data
from db_dataclasses import (Filmwork, Genre, GenreFilmwork, Person,
                            PersonFilmwork)
from my_logging import logger

load_dotenv()

dsn = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=content',
}

from_db = 'db.sqlite'
tables = ['genre', 'person', 'film_work', 'genre_film_work', 'person_film_work']


class SQLiteConnection:
    def __init__(self, db: str) -> None:
        self.db = db

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def __exit__(self, ex_type: Union[Type[BaseException], None], ex_val: str, ex_tb: str) -> None:
        if ex_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


class PostgresConnection:
    def __init__(
            self, dbname: str, user: str, password: str, host: str, port: int, options: str
    ) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.options = options

    def __enter__(self) -> connection:
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                     host=self.host, port=self.port, options=self.options)
        return self.conn

    def __exit__(self, ex_type: Union[Type[BaseException], None], ex_val: str, ex_tb: str) -> None:
        if ex_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    with PostgresConnection(**dsn) as pg_conn:
        for table in tables:
            with SQLiteConnection(from_db) as sqlite_conn:
                extractor = SQLiteExtractor(sqlite_conn)
                records = []
                curs_pg = pg_conn.cursor()

                for chunk in extractor.extract(table):
                    try:
                        for row in chunk:
                            if table == 'genre':
                                record = Genre(*row)
                                records.append(record)
                            if table == 'person':
                                record = Person(*row)
                                records.append(record)
                            if table == 'film_work':
                                record = Filmwork(*row)
                                records.append(record)
                            if table == 'genre_film_work':
                                record = GenreFilmwork(*row)
                                records.append(record)
                            if table == 'person_film_work':
                                record = PersonFilmwork(*row)
                                records.append(record)

                    except Exception as e:
                        logger.exception(f'Error occurred when saving to {table}: {e}')
                        raise SystemExit

                    load_data(curs_pg, records, table)
                    pg_conn.commit()
