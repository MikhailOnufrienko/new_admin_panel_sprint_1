import os
import sqlite3
from typing import Type, Union

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection

from data_extractor import SQLiteExtractor
from data_loader import load_data
from db_dataclasses import (Genre, GenreFilmwork, Filmwork,
                            Person, PersonFilmwork)
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

    def __exit__(
            self,
            ex_type: Union[Type[BaseException], None],
            ex_val: str,
            ex_tb: str
    ) -> None:
        if ex_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


class PostgresConnection:
    def __init__(
            self,
            dbname: str,
            user: str,
            password: str,
            host: str,
            port: int,
            options: str
    ) -> None:
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.options = options

    def __enter__(self) -> connection:
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            options=self.options)
        return self.conn

    def __exit__(self,
                 ex_type: Union[Type[BaseException], None],
                 ex_val: str,
                 ex_tb: str
    ) -> None:
        if ex_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


def prepare_data(field: str) -> str:
    """Modify the name of the given table field if
    it presents in fields_mapping dict.

    """

    fields_mapping = {
        'created_at': 'created',
        'updated_at': 'modified',
    }
    if field in list(fields_mapping.keys()):
        return fields_mapping[field]
    return field


def append_target_record(table_name: str) -> None:
    """Append a record to the given table.

    """

    table_to_dataclass = {
        'genre': Genre,
        'person': Person,
        'film_work': Filmwork,
        'genre_film_work': GenreFilmwork,
        'person_film_work': PersonFilmwork
    }

    dataclass_name = table_to_dataclass[table_name]
    target_record = dataclass_name(**target_record_dict)
    target_records.append(target_record)


if __name__ == '__main__':
    with PostgresConnection(**dsn) as pg_conn:
        for table in tables:
            with SQLiteConnection(from_db) as sqlite_conn:
                extractor = SQLiteExtractor(sqlite_conn)
                target_records = []
                curs_pg = pg_conn.cursor()

                for chunk in extractor.extract(table):
                    try:
                        for row in chunk:
                            target_record_dict = {}
                            source_data = dict(**row)
                            for field_name, field_value in source_data.items():
                                target_field_name = prepare_data(field_name)
                                target_record_dict[target_field_name] = field_value
                            append_target_record(table)
                    except Exception as e:
                        logger.exception('Error occurred when saving to %s: {%s}', table, e)
                        raise SystemExit
                    load_data(curs_pg, target_records, table)
                    pg_conn.commit()
