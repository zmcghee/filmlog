from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^seen(\d{4}).html', 'filmlog.views.films_seen_by_year'),
	url(r'^ondeck.html', 'django.views.generic.simple.direct_to_template', {'template': 'ondeck.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
