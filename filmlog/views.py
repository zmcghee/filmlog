from django.http import Http404
from django.shortcuts import render

from filmlog.models import Entry

def films_seen_by_year(request, year=None):
	try:
		year = int(year)
		if year < 2010:
			raise Http404
	except TypeError:
		from datetime import datetime
		year = datetime.today().year
	entries = Entry.objects.filter(date__year=year).order_by('pk')
	context = {'entries': entries,
			   'imax': ['I', 'L'],
			   'year': year,
			   'total': range(0,10)
			  }
	return render(request, 'films_seen_by_year.html', context)
