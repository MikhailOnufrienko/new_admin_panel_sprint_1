from dataclasses import asdict, dataclass, fields
from typing import Type

from psycopg2.extensions import cursor
from psycopg2.extras import execute_batch


FIELDS_MAPPING = {
    'id': 'id',
    'created_at': 'created',
    'updated_at': 'modified',
    'name': 'name',
    'full_name': 'full_name',
    'description': 'description',
    'role': 'role'
}


def load_data(curs: cursor, records: list[Type[dataclass]], table: str) -> None:
    """Write the extracted data to a PostgreSQL database.

    """

    curs.execute(f'TRUNCATE {table};')
    columns = tuple(asdict(records[0]).keys())
    columns_no_quotes = ','.join(tuple(asdict(records[0]).keys()))
    placeholders = ', '.join(['%s'] * len(columns))
    query = f'INSERT INTO {table} ({columns_no_quotes}) VALUES ({placeholders})'
    vals = []
    for record in records:
        data = asdict(record)
        vals.append(tuple(data.values()))
    execute_batch(curs, query, vals)
