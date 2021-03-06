from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', lambda r: redirect('http://about.me/zmcghee')),
	url(r'^movies$', 'filmlog.views.films_seen_this_year'),
	url(r'^movies/filmlog.css', 'django.views.generic.simple.direct_to_template', {'template': 'filmlog.css', 'mimetype': 'text/css'}),
	url(r'^movies/(\d{4})/(\d{2})$', 'filmlog.views.films_seen_by_year'),
	url(r'^movies/(\d{4})$', 'filmlog.views.films_seen_by_year'),
	url(r'^movies/visual/(\d{4})/(\d{2})$', 'filmlog.views.html_month'),
	url(r'^movies/visual/(\d{4})$', 'filmlog.views.html_year'),
	url(r'^movies/api/(\d{4})/(\d{2})$', 'filmlog.views.json_month'),
	url(r'^movies/api/(\d{4})$', 'filmlog.views.json_year'),
	url(r'^movies/ondeck.html', 'django.views.generic.simple.direct_to_template', {'template': 'ondeck.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
