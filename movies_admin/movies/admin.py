from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0
    verbose_name = _('genre filmwork')


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)
    extra = 0
    verbose_name = _('person filmwork')


@register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created',)


@register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified',)
    search_fields = ('full_name',)
    ordering = ['-modified']


@register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)
    list_display = ('title', 'description', 'type', 'creation_date', 'rating',)
    empty_value_display = '-empty-'
    list_filter = ('type',)
    search_fields = ('title',)
