from django.contrib import admin
from .models import Genre, Filmwork, Person, GenreFilmwork, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person',)
    extra = 0


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'created', 'modified',)
    search_fields = ('full_name',)
    ordering = ['-modified']


class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline,)
    list_display = ('title', 'description', 'type', 'creation_date', 'rating',)
    empty_value_display = '-empty-'
    list_filter = ('type',)
    search_fields = ('title',)


admin.site.register(Genre, GenreAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Filmwork, FilmworkAdmin)
