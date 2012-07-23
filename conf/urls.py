from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^movies/(\d{4})$', 'filmlog.views.films_seen_by_year'),
	url(r'^movies/visual/(\d{4})/(\d{2})$', 'filmlog.views.html_month'),
	url(r'^movies/visual/(\d{4})$', 'filmlog.views.html_year'),
	url(r'^movies/api/(\d{4})/(\d{2})$', 'filmlog.views.json_month'),
	url(r'^movies/api/(\d{4})$', 'filmlog.views.json_year'),
	url(r'^movies/ondeck.html', 'django.views.generic.simple.direct_to_template', {'template': 'ondeck.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
