import psycopg2
from dataclasses import asdict


def load_data(records, table, **dsn):
    conn = psycopg2.connect(**dsn)
    curs = conn.cursor()
    curs.execute(f"TRUNCATE {table};")

    for record in records:
        data = asdict(record)
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f'''INSERT INTO {table} ({columns})
                    VALUES ({placeholders})
                 '''
        curs.execute(query, tuple(data.values()))
    conn.commit()
    conn.close()
