from django.db import models
import uuid
from .mixins import UUIDMixin, TimeStampedMixin
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(UUIDMixin, TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField('Имя')

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class TypeChoices(models.TextChoices):
        MOVIE = 'Фильм', 'Фильм'
        TV_SHOW = 'Сериал', 'Сериал'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField('Название')
    description = models.TextField('Описание', blank=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    creation_date = models.DateField('Дата выхода'),
    rating = models.FloatField('Рейтинг', blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]),
    type = models.TextField('Тип', choices=TypeChoices.choices, default=TypeChoices.MOVIE),
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name='Персона')
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name='Фильм')
    role = models.TextField('Роль')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
