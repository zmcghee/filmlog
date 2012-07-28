import datetime

from filmlog.models import Entry, Venue

def stats(start_date, end_date):
	entries = Entry.objects.between(start_date, end_date)
	first_timers = entries.exclude(repeat=True)
	all_venues = [{
		'name': 'Alamo Drafthouse',
		'total': entries.filter(venue__in=Venue.objects.alamo(True)).count()
	}]
	for venue in Venue.objects.theatrical(True).alamo(False):
		all_venues.append({
			'name': venue.name,
			'total': venue.entries.between(start_date, end_date).count()
		})
	release_year_threshold = int(start_date[:4])-2
	stats = {
		'venues': {
			'all': all_venues,
			'alamo': [{'name': venue.name,
					   'total': venue.entries.between(start_date, end_date).count()}
					   for venue in Venue.objects.alamo(True)]
		},
		'thumb': {
			'all': {
				'up': entries.filter(recommended=True).count(),
				'down': entries.filter(recommended=False).count()
			},
			'first_timers': {
				'up': first_timers.filter(recommended=True).count(),
				'down': first_timers.exclude(walkout=True).filter(recommended=False).count()
			}
		},
		'total_seen': entries.exclude(walkout=True).count(),
		'walkouts': entries.filter(walkout=True).count(),
		'in_3d': entries.filter(in_3d=True).count(),
		'first_timers': first_timers.exclude(walkout=True).count(),
		'repeats': entries.exclude(walkout=True).filter(repeat=True).count(),
		'release_year': {
			'threshold': release_year_threshold,
			'repertory': entries.filter(movie__premiere_year__lt=release_year_threshold).count(),
			'current': entries.filter(movie__premiere_year__gte=release_year_threshold).count()
		}
	}
	if start_date[:7] == end_date[:7]:
		stats['dates'] = Entry.objects.day_count(start_date, end_date, allow_gaps=False, json=True)
		stats['title'] = "%s %s" % (stats['dates'][0]['month'], stats['dates'][0]['year'])
	else:
		today = datetime.date.today()
		stats['months'] = Entry.objects.month_count(start_date, end_date, allow_gaps=False, json=True)
		if (start_date[:4] == end_date[:4]) and (
			len(stats['months']) == 12 or (
				int(end_date[:4])==today.year and len(stats['months'])==today.month
			)
		):
			stats['title'] = str(stats['months'][0]['year'])
		else:
			stats['title'] = "%s thru %s" % (start_date, end_date)
	return stats
