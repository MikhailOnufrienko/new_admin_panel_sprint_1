import sqlite3


class SQLiteExtractor:
    def __init__(self, db_file, chunk_size=66):
        self.conn = sqlite3.connect(db_file)
        self.chunk_size = chunk_size

    def extract(self, table, columns):
        curs = self.conn.cursor()
        query = f"SELECT {','.join(columns)} FROM {table}"
        curs.execute(query)

        while True:
            results = curs.fetchmany(self.chunk_size)
            if not results:
                break
            yield results

    def close(self):
        self.conn.close()
