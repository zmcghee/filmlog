import datetime

from django.conf import settings
from django.db import connection, models, transaction

from filmlog.utils import dates_between, months_between

class EntryQuerySet(models.query.QuerySet):
	def film(self):
		return self.filter(format__in=['0','I','S'])

	def digital(self, theatrical_only=False, video_only=False):
		from filmlog.models import Venue
		entries = self.exclude(format__in=['0','I','S'])
		theatrical_filter = {'venue__in': Venue.objects.theatrical(True)}
		if theatrical_only:
			entries = entries.filter(**theatrical_filter)
		if video_only:
			entries = entries.exclude(**theatrical_filter)
		return entries

	def theatrical(self):
		from filmlog.models import Venue
		return self.filter(venue__in=Venue.objects.theatrical(True))

	def video(self):
		from filmlog.models import Venue
		return self.exclude(venue__in=Venue.objects.theatrical(True))

class EntryManager(models.Manager):
	def get_query_set(self):
		model = models.get_model('filmlog', 'Entry')
		return EntryQuerySet(model)

	def __getattr__(self, attr, *args):
		try:
			return getattr(self.__class__, attr, *args)
		except AttributeError:
			return getattr(self.get_query_set(), attr, *args)

	@property
	def walkout_list(self):
		return self.get_query_set().filter(walkout=True).values_list('movie', flat=True)

	@property
	def year_list(self):
		cursor = connection.cursor()
		if 'sqlite' in settings.DATABASES['default']['ENGINE']:
			cursor.execute("SELECT DISTINCT STRFTIME('%%Y', date) AS year FROM filmlog_entry;")
		elif 'mysql' in settings.DATABASES['default']['ENGINE']:
			cursor.execute("SELECT DISTINCT date_format(date, '%Y') AS year FROM filmlog_entry;")
		else:
			raise NotImplementedError("EntryManager.year_list custom SQL query not implemented for this backend.")
		return [int(row[0]) for row in cursor.fetchall()]

	@property
	def month_list(self):
		return self.month_list_for_year(None)

	def month_list_for_year(self, year):
		cursor = connection.cursor()
		if 'sqlite' in settings.DATABASES['default']['ENGINE']:
			sql = "SELECT DISTINCT STRFTIME('%%Y/%%m', date) AS month, case STRFTIME('%%m', date) when '01' then 'January' when '02' then 'February' when '03' then 'March' when '04' then 'April' when '05' then 'May' when '06' then 'June' when '07' then 'July' when '08' then 'August' when '09' then 'September' when '10' then 'October' when '11' then 'November' when '12' then 'December' else '' end AS month_name, STRFTIME('%%Y', date) AS year"
		elif 'mysql' in settings.DATABASES['default']['ENGINE']:
			sql = "SELECT DISTINCT date_format(date, '%Y/%m') as month, date_format(date, '%M') AS month_name, date_format(date, '%Y') as year"
		else:
			raise NotImplementedError("EntryManager.month_list custom SQL query not implemented for this backend.")
		sql += " FROM filmlog_entry"
		if year is not None:
			sql += " WHERE date >= '%s-01-01' AND date <= '%s-12-31'" % (int(year), int(year))
		cursor.execute(sql)
		return [{'month': row[0], 'month_name': row[1], 'year': row[2], 'month_and_year': "%s %s" % (row[1], row[2])} for row in cursor.fetchall()]

	def between(self, start_date, end_date):
		return self.filter(date__gte=start_date, date__lte=end_date)

	def day_count(self, start_date, end_date, allow_gaps=True, json=True):
		if not isinstance(start_date, basestring):
			start_date = "%04d-%02d-01" % (start_date.year, start_date.month, 
			  start_date.day)
		if not isinstance(end_date, basestring):
			end_date = "%04d-%02d-01" % (end_date.year, end_date.month, end_date.day)
		start_year, start_month, start_day = [int(a) for a in start_date.split("-")]
		end_year, end_month, end_day = [int(a) for a in end_date.split("-")]
		sql = """SELECT id, date, COUNT(date) as total
				 FROM `filmlog_entry`
				 WHERE date >= '%04d-%02d-%02d' AND date <= '%04d-%02d-%02d'
				 GROUP BY date""" % (
				 	start_year, start_month, start_day,
				 	end_year, end_month, end_day
				 )
		result = self.raw(sql)
		if allow_gaps:
			if json:
				return [{'date': str(row.date), 'total': row.total} for row in result]
			return [(row.date, row.total) for row in result]
		dates = []
		last_date = datetime.date(start_year, start_month, start_day)
		for row in result:
			if (row.date - last_date).days > 1:
				for date in dates_between(last_date, row.date):
					if json:
						dates.append({'year': date.year, 'month': date.strftime("%B"),
									  'month_abbr': date.strftime("%b"),
									  'date': str(date), 'total': 0})
					else:
						dates.append((date, 0))
			if json:
				dates.append({'year': row.date.year, 'month': row.date.strftime("%B"),
							  'month_abbr': row.date.strftime("%b"),
							  'date': str(row.date), 'total': row.total})
			else:
				dates.append((row.date, row.total))
			last_date = row.date
		return dates

	def month_count(self, start_month, end_month, allow_gaps=True, json=False):
		if not isinstance(start_month, basestring):
			start_month = "%04d-%02" % (start_month.year, start_month.month)
		if not isinstance(end_month, basestring):
			end_month = "%04d-%02d" % (end_month.year, end_month.month)
		start_year, start_month = [int(a) for a in start_month.split("-")[:2]]
		end_year, end_month = [int(a) for a in end_month.split("-")[:2]]
		if 'sqlite' in settings.DATABASES['default']['ENGINE']:
			sql = """SELECT id, date, month, COUNT(month) as total FROM (
						SELECT id, date, strftime('%%%%m', date) as month
						FROM `filmlog_entry`
						WHERE date >='%04d-%02d-01' AND date <='%04d-%02d-31'
						ORDER BY date DESC 
					 )
					 GROUP BY month""" % (start_year, start_month, end_year, end_month)
		elif 'mysql' in settings.DATABASES['default']['ENGINE']:
			sql = """SELECT id, date, month, COUNT(month) as total FROM (
						SELECT id, date, date_format(date, '%%%%m') as month
						FROM `filmlog_entry`
						WHERE date >='%04d-%02d-01' AND date <='%04d-%02d-31'
						ORDER BY date DESC 
					 ) as a
					 GROUP BY month""" % (start_year, start_month, end_year, end_month)
		else:
			raise NotImplementedError("EntryManager.year_list custom SQL query not implemented for this backend.")
		result = self.raw(sql)
		if allow_gaps:
			if json:
				return [{'date': str(row.date), 'total': row.total} for row in result]
			return [(row.date, row.total) for row in result]
		months = []
		try:
			last_date = datetime.date(start_year, start_month-1, 1)
		except ValueError:
			last_date = datetime.date(start_year-1, 12, 1)
		for row in result:
			if (row.date - last_date).days > 28:
				for month in months_between(last_date, row.date):
					date = datetime.date(*(int(a) for a in month.split("-")+[1]))
					if json:
						months.append({'year': date.year, 'month': date.strftime("%B"),
									   'month_abbr': date.strftime("%b"),
									   'date': str(date), 'total': 0})
					else:
						months.append((date, 0))
			if json:
				months.append({'year': row.date.year, 'month': row.date.strftime("%B"),
							   'month_abbr': row.date.strftime("%b"),
							   'date': str(row.date), 'total': row.total})
			else:
				months.append((row.date, row.total))
			last_date = row.date
		return months
	
	def year_count(self, start_year, end_year, allow_gaps=True, json=False):
		start_year = int(start_year)
		end_year = int(end_year)
		sql = """SELECT id, date, year, COUNT(year) as total FROM (
					SELECT id, date, strftime('%%%%Y', date) as year
					FROM `filmlog_entry`
					WHERE date >='%04d-01-01' AND date <='%04d-12-31'
					ORDER BY date DESC 
				 )
				 GROUP BY year""" % (start_year, end_year)
		result = self.raw(sql)
		if allow_gaps:
			if json:
				return [{'date': int(row.year), 'total': row.total} for row in result]
			return [(row.year, row.total) for row in result]
		years = []
		last_year = start_year - 1
		for row in result:
			if (int(row.year) - last_year) > 1:
				for year in range(last_year, int(row.year))[1:]:
					if json:
						years.append({'year': year, 'total': 0})
					else:
						years.append((year, 0))
			if json:
				years.append({'year': int(row.year), 'total': row.total})
			else:
				years.append((int(row.year), row.total))
			last_year = int(row.year)
		return years

class VenueQuerySet(models.query.QuerySet):
	def theatrical(self, filter_or_exclude):
		try:
			assert type(filter_or_exclude) == bool
		except AssertionError:
			raise TypeError("alamo method expects boolean")
		theatrical_filter = {'city__exact': ''}
		if not filter_or_exclude:
			return self.filter(**theatrical_filter)
		return self.exclude(**theatrical_filter)
	
	def alamo(self, filter_or_exclude):
		try:
			assert type(filter_or_exclude) == bool
		except AssertionError:
			raise TypeError("alamo method expects boolean")
		alamo_filter = {'name__startswith': 'Alamo Drafthouse'}
		if not filter_or_exclude:
			return self.exclude(**alamo_filter)
		return self.filter(**alamo_filter)

class VenueManager(models.Manager):
	def get_query_set(self):
		model = models.get_model('filmlog', 'Venue')
		return VenueQuerySet(model)

	def __getattr__(self, attr, *args):
		try:
			return getattr(self.__class__, attr, *args)
		except AttributeError:
			return getattr(self.get_query_set(), attr, *args)