import datetime, json

from calendar import monthrange

from django.http import Http404, HttpResponse
from django.shortcuts import render

from filmlog.api import stats
from filmlog.models import Entry, Venue

def films_seen_by_year(request, year=None):
	try:
		year = int(year)
		if (year < 2010) or (year > datetime.datetime.today().year):
			raise Http404
	except TypeError:
		year = datetime.datetime.today().year
	entries = Entry.objects.filter(date__year=year)
	total = entries.filter(walkout=False).count()
	order_by = request.GET.get('order', None)
	if order_by == 'date':
		entries = entries.order_by('pk')
	elif order_by == 'title':
		entries = entries.order_by('movie__title_sans_article')
	elif order_by == 'rating':
		entries = entries.order_by('walkout', '-recommended', 'movie__title_sans_article', 'pk')
	else:
		entries = entries.order_by('-pk')
		order_by = 'reverse'
	context = {'entries': entries,
			   'imax': ['I', 'L'],
			   'year': year,
			   'total': total,
			   'order_by': order_by,
			   'years': Entry.objects.year_list
			  }
	return render(request, 'films_seen_by_year.html', context)

def json_api(request, *args):
	context = stats(*args)
	return HttpResponse(json.dumps(context))

def html_date_range(request, *args):
	context = stats(*args)
	return render(request, 'charts.html', context)

def html_month(request, year, month):
	start_date = "%s-%s-01" % (year, month)
	last_day_of_month = monthrange(int(year), int(month))[1]
	end_date = "%s-%s-%s" % (year, month, last_day_of_month)
	return html_date_range(request, start_date, end_date)

def html_year(request, year):
	start_date = "%s-01-01" % year
	end_date = "%s-12-31" % year
	return html_date_range(request, start_date, end_date)
