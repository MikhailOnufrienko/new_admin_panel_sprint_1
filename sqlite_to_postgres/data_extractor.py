from sqlite3 import Connection


class SQLiteExtractor:
    """A class to represent the mechanism of extracting data
    from an SQLite database.

    Data are extracted by chunks.
    """
    def __init__(self, conn: Connection, chunk_size: int = 1000) -> None:
        self.conn = conn
        self.chunk_size = chunk_size

    def extract(self, table: str) -> list:
        curs = self.conn.cursor()
        try:
            query = f'SELECT * FROM {table}'
            curs.execute(query)
        except ValueError:
            print(f'No such table: {table}')
        while True:
            results = curs.fetchmany(self.chunk_size)
            if not results:
                break
            yield results
