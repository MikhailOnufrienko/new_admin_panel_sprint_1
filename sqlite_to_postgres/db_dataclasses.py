from uuid import UUID
from dataclasses import dataclass
from datetime import datetime, date


@dataclass()
class Genre:
    id: UUID
    name: str
    description: str
    created: datetime
    modified: datetime


@dataclass()
class Person:
    id: UUID
    full_name: str
    created: datetime
    modified: datetime


@dataclass()
class Filmwork:
    id: UUID
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created: datetime
    modified: datetime
    file_path: str


@dataclass()
class GenreFilmwork:
    id: UUID
    genre_id: UUID
    film_work_id: UUID
    created: datetime


@dataclass()
class PersonFilmwork:
    id: UUID
    person_id: UUID
    film_work_id: UUID
    role: str
    created: datetime
