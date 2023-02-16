from dataclasses import asdict, dataclass
from typing import Type

from psycopg2.extensions import cursor


def load_data(curs: cursor, records: Type[dataclass], table: str) -> None:
    """Write the extracted data to a PostgreSQL database.

    """

    curs.execute(f'TRUNCATE {table};')

    for record in records:
        data = asdict(record)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        curs.execute(query, tuple(data.values()))
