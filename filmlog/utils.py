import datetime

def dates_between(start, end):
	r = (end+datetime.timedelta(days=1)-start).days
	return [start+datetime.timedelta(days=i) for i in range(r)][1:-1]

def months_between(start, end):
	dates = dates_between(start, end)
	months = ["%d-%d" % (start.year, start.month),
			  "%d-%d" % (end.year, end.month)]
	for date in dates:
		month = "%d-%d" % (date.year, date.month)
		if month not in months:
			months.append(month)
	return months[2:]
