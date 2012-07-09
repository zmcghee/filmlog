import datetime, json

from django.http import Http404, HttpResponse
from django.shortcuts import render

from filmlog.models import Entry, Venue

def films_seen_by_year(request, year=None):
	try:
		year = int(year)
		if (year < 2010) or (year > datetime.datetime.today().year):
			raise Http404
	except TypeError:
		year = datetime.datetime.today().year
	entries = Entry.objects.filter(date__year=year).order_by('pk')
	context = {'entries': entries,
			   'imax': ['I', 'L'],
			   'year': year,
			   'total': range(0,10)
			  }
	return render(request, 'films_seen_by_year.html', context)

def data(request, start_date, end_date):
	context = {
		'venues': {}
	}
	date_filter = {'date__gte': start_date, 'date__lte': end_date}
	entries = Entry.objects.filter(**date_filter)
	# Venues
	alamo_filter = {'name__startswith': 'Alamo Drafthouse'}
	theatrical_venues = Venue.objects.exclude(city__exact='')
	all_alamo_venues = theatrical_venues.filter(**alamo_filter)
	non_alamo_venues = theatrical_venues.exclude(**alamo_filter)
	context['venues']['all'] = [{
		'name': 'Alamo Drafthouse',
		'total': Entry.objects.filter(**date_filter).filter(venue__name__startswith='Alamo Drafthouse').count()
	}]
	for venue in non_alamo_venues.all():
		context['venues']['all'].append({
			'name': venue.name,
			'total': venue.entries.filter(**date_filter).count()
		})
	context['venues']['alamo'] = []
	for venue in all_alamo_venues.all():
		context['venues']['alamo'].append({
			'name': venue.name,
			'total': venue.entries.filter(**date_filter).count()
		})
	# Movies I've liked
	first_timers = entries.exclude(repeat=True)
	context['thumb'] = {
		'all': {
			'up': entries.filter(recommended=True).count(),
			'down': entries.filter(recommended=False).count()
		},
		'first_timers': {
			'up': first_timers.filter(recommended=True).count(),
			'down': first_timers.exclude(walkout=True).filter(recommended=False).count()
		}
	}
	# Other stuff
	context['total_seen'] = entries.exclude(walkout=True).count()
	context['walkouts'] = first_timers.filter(walkout=True).count()
	context['in_3d'] = entries.filter(in_3d=True).count()
	context['first_timers'] = first_timers.exclude(walkout=True).count()
	context['repeats'] = entries.exclude(walkout=True).filter(repeat=True).count()
	# Number of entries per day
	day_count = Entry.objects.raw("SELECT id, date, COUNT(date) as total FROM `filmlog_entry` WHERE date >= '%s' AND date <= '%s' GROUP BY date" % (start_date, end_date))
	context['dates'] = []
	def dates_between(start, end):
		r = (end+datetime.timedelta(days=1)-start).days
		return [start+datetime.timedelta(days=i) for i in range(r)][1:-1]
	for row in day_count:
		try:
			if (row.date - last_date).days > 1:
				for date in dates_between(last_date, row.date):
					context['dates'].append({
						'date': "%s-%s-%s" % (date.year, date.month, date.day),
						'total': 0
					})
		except NameError:
			pass #first time, nbd
		context['dates'].append({
			'date': "%s-%s-%s" % (row.date.year, row.date.month, row.date.day),
			'total': row.total
		})
		last_date = row.date
	return context

def json_api(*args):
	context = data(*args)
	return HttpResponse(json.dumps(context))

def html(request, *args):
	context = data(request, *args)
	return render(request, 'charts.html', context)

def html_this_year(request):
	this_year = datetime.datetime.today().year
	start_date = "%s-01-01" % this_year
	end_date = "%s-12-31" % this_year
	return html(request, start_date, end_date)