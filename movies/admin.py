from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified',)
    search_fields = ('full_name',)


class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'description', 'type', 'creation_date', 'rating',)
    empty_value_display = '-empty-'
    list_filter = ('type',)
    search_fields = ('title',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Filmwork, FilmworkAdmin)
