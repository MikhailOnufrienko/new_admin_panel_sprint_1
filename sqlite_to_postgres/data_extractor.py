class SQLiteExtractor:
    """A class to represent the mechanism of extracting data
    from an SQLite database.

    The data are extracted by chunks.
    """
    def __init__(self, conn, chunk_size=1000):
        self.conn = conn
        self.chunk_size = chunk_size

    def extract(self, table):
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
