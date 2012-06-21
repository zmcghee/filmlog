from django.contrib import admin

from filmlog.models import Director, Movie, Venue, Entry

class DirectorAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name', 'imdb',)
	list_display_links = ('pk',)
	list_editable = ('name', 'imdb',)
	search_fields = ['name', 'imdb',]

class MovieAdmin(admin.ModelAdmin):
	filter_horizontal = ('directors',)
	list_display = ('pk', 'title', 'premiere_year', 'nyc_release_year', 'imdb',)
	list_display_links = ('pk', 'title',)
	list_editable = ('premiere_year', 'nyc_release_year', 'imdb',)
	list_filter = ('premiere_year', 'nyc_release_year',)
	search_fields = ['title_sans_article', 'imdb', 'directors',]

class EntryAdmin(admin.ModelAdmin):
	date_hierarchy = 'date'
	list_display = ('pk', 'date', 'movie', 'venue', 'format', 'in_3d', 'repeat', 'walkout',)
	list_display_links = ('pk',)
	list_editable = ('movie', 'venue', 'format', 'in_3d', 'repeat', 'walkout',)
	list_filter = ('venue', 'format', 'in_3d', 'repeat', 'movie__premiere_year', 'movie__nyc_release_year',)
	raw_id_fields = ('movie',)
	search_fields = ['movie__title_sans_article', 'movie__imdb', 'movie__directors',]

admin.site.register(Director, DirectorAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Venue)
admin.site.register(Entry, EntryAdmin)
