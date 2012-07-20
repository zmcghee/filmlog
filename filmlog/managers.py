from django.db import connection, models, transaction

class EntryManager(models.Manager):
	@property
	def walkout_list(self):
		return self.get_query_set().filter(walkout=True).values_list('movie', flat=True)

	@property
	def year_list(self):
		cursor = connection.cursor()
		cursor.execute("SELECT DISTINCT STRFTIME('%%Y', date) AS year FROM filmlog_entry;")
		return [int(row[0]) for row in cursor.fetchall()]