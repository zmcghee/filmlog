import datetime, json

from calendar import monthrange

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from filmlog.api import stats
from filmlog.models import Entry, Venue

def films_seen_this_year(request):
	return redirect('/movies/%s' % datetime.datetime.today().year)

def films_seen_by_year(request, year=None, month=None):
	try:
		year = int(year)
		if (year < 2010) or (year > datetime.datetime.today().year):
			raise Http404
	except TypeError:
		year = datetime.datetime.today().year
	entries = Entry.objects.filter(date__year=year)
	if month:
		if year == datetime.datetime.today().year and int(month) > datetime.datetime.today().month:
			raise Http404
		entries = entries.filter(date__month=month)
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
	if not month:
		start_date = "%s-01-01" % year
		end_date = "%s-12-31" % year
	else:
		start_date = "%s-%s-01" % (year, month)
		last_day_of_month = monthrange(int(year), int(month))[1]
		end_date = "%s-%s-%s" % (year, month, last_day_of_month)
	context = {'entries': entries,
			   'imax': ['I', 'L'],
			   'year': year,
			   'total': total,
			   'order_by': order_by,
			   'years': Entry.objects.year_list,
			   'stats': stats(start_date, end_date),
			   'months': Entry.objects.month_list_for_year(year)
			  }
	return render(request, 'films_seen_by_year.html', context)

def json_date_range(request, *args):
	context = stats(*args)
	return HttpResponse(json.dumps(context), content_type='application/json')

def json_month(request, year, month):
	start_date = "%s-%s-01" % (year, month)
	last_day_of_month = monthrange(int(year), int(month))[1]
	end_date = "%s-%s-%s" % (year, month, last_day_of_month)
	return json_date_range(request, start_date, end_date)

def json_year(request, year):
	start_date = "%s-01-01" % year
	end_date = "%s-12-31" % year
	return json_date_range(request, start_date, end_date)

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
