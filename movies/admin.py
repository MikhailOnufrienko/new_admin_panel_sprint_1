from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created',)


class PersonAdmin(admin.ModelAdmin):
    pass


class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'description', 'type', 'creation_date', 'rating',)
    empty_value_display = '-empty-'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Filmwork, FilmworkAdmin)
