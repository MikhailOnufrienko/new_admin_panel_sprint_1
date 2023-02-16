from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass()
class UUIDMixin:
    id: UUID


@dataclass()
class TimeStampedMixin:
    created: datetime
    modified: datetime


@dataclass()
class Genre(UUIDMixin, TimeStampedMixin):
    name: str
    description: str


@dataclass()
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str


@dataclass()
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str
    description: str
    creation_date: date
    file_path: str
    rating: float
    type: str


@dataclass()
class GenreFilmwork(UUIDMixin):
    film_work_id: UUID
    genre_id: UUID
    created: datetime


@dataclass()
class PersonFilmwork(UUIDMixin):
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime
