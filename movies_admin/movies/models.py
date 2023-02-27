from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampedMixin, UUIDMixin


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.TextField(_('Title'))
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('Name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        indexes = [
            models.Index(fields=['full_name'], name='person_idx')
        ]

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class Types(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.TextField(_('Title'))
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_('Creation date'))
    rating = models.FloatField(_('Rating'), blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.TextField(_('Type'), choices=Types.choices, default=Types.MOVIE)
    file_path = models.FileField(_('File'), blank=True, null=True, upload_to='movies/')
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        indexes = [
            models.Index(fields=['title'], name='film_work_title_idx'),
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx')
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'genre_id'],
                         name='film_work_genre_idx')
        ]


class PersonFilmwork(UUIDMixin):
    class Roles(models.TextChoices):
        ACTOR = 'actor', _('actor')
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Персона')
    film_work = models.ForeignKey(Filmwork, on_delete=models.CASCADE, verbose_name='Фильм')
    role = models.TextField(_('Role'), choices=Roles.choices, default=Roles.ACTOR)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'],
                         name='film_work_person_role_idx')
        ]
