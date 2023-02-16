import sqlite3
from sqlite3 import Connection
from my_logging import logger


class SQLiteExtractor:
    """A class to represent the mechanism of extracting data
    from an SQLite database.

    Data are extracted by chunks.
    """
    def __init__(self, conn: Connection, chunk_size: int = 1000) -> None:
        self.conn = conn
        self.chunk_size = chunk_size

    def extract(self, table: str) -> list[sqlite3.Row]:
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        try:
            query = f'SELECT * FROM {table}'
            curs.execute(query)
        except sqlite3.OperationalError:
            logger.error('No such table: %s', table, exc_info=True)
            raise SystemExit
        while True:
            results = curs.fetchmany(self.chunk_size)
            if not results:
                break
            yield results
