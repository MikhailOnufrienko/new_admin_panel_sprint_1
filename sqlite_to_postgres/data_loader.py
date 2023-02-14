from dataclasses import asdict


def load_data(curs, records, table):
    """Write the extracted data to a PostgreSQL database.

    """

    curs.execute(f'TRUNCATE {table};')

    for record in records:
        data = asdict(record)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        curs.execute(query, tuple(data.values()))
