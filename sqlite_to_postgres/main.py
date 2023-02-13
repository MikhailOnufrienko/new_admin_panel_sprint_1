from data_extractor import SQLiteExtractor
from data_loader import load_data
from db_dataclasses import Genre, Person, Filmwork, GenreFilmwork, PersonFilmwork


dsn = {
    "dbname": "movies_database",
    "user": "postgres",
    "password": "GhastangsTmihan13",
    "host": "127.0.0.1",
    "port": 5432,
    "options": "-c search_path=content",
}

from_table = "person"
to_table = "person"
from_fields = ["id", "full_name", "created_at", "updated_at"]

if __name__ == "__main__":
    extractor = SQLiteExtractor("db.sqlite")
    records = []
    for chunk in extractor.extract(from_table, from_fields):
        for row in chunk:
            record = Person(*row)
            records.append(record)
        load_data(records, to_table, **dsn)
    extractor.close()
