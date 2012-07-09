from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^seen(\d{4}).html', 'filmlog.views.films_seen_by_year'),
	url(r'^visual/(\d{4}-\d{2}-\d{2})/(\d{4}-\d{2}-\d{2})/', 'filmlog.views.html'),
	url(r'^visual/$', 'filmlog.views.html_this_year'),
	url(r'^api/(\d{4}-\d{2}-\d{2})/(\d{4}-\d{2}-\d{2})/', 'filmlog.views.json_api'),
	url(r'^ondeck.html', 'django.views.generic.simple.direct_to_template', {'template': 'ondeck.html'}),
    url(r'^admin/', include(admin.site.urls)),
)
