from django.contrib import admin

from filmlog.models import Director, Movie, Venue, Entry

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Venue)
admin.site.register(Entry)