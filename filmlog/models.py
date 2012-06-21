from django.db import models

FORMATS = (('0', '35mm'), ('1', 'DCP'), ('2', 'Blu-ray'), ('3', 'DVD'),
           ('4', 'File/Download'), ('6', 'Streaming'), ('8', 'Broadcast/VOD'),
           ('I', 'IMAX (Film)'), ('L', 'IMAX (Digital)'), ('S', '70mm'),)

class Director(models.Model):
	name = models.CharField(max_length=100, db_index=True)
	imdb = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('name',)

class Movie(models.Model):
	title_sans_article = models.CharField(max_length=250, db_index=True)
	leading_article = models.CharField(max_length=3, null=True, blank=True)
	imdb = models.IntegerField(null=True, blank=True)
	premiere_year = models.CharField(max_length=4)
	nyc_release_year = models.CharField(max_length=4, null=True, blank=True)
	directors = models.ManyToManyField(Director, related_name='movies')

	def set_title(self, complete_title):
		articles = ("A", "AN", "THE", "EL", "LA", "LE", "IL", "L'")
		try:
			article, title = complete_title.split(" ", 1)
		except ValueError:
			article = ''
		if article.upper() in articles:
			self.leading_article = article
			self.title_sans_article = title
		else:
			self.leading_article = ''
			self.title_sans_article = complete_title

	def get_title(self):
		if not self.leading_article:
			return self.title_sans_article
		return "%s %s" % (self.leading_article, self.title_sans_article)

	title = property(get_title, set_title)

	def __unicode__(self):
		return "%s (%s)" % (self.title, self.premiere_year)

	class Meta:
		ordering = ('title_sans_article', 'leading_article', 'premiere_year',)

class Venue(models.Model):
	name = models.CharField(max_length=100)
	city = models.CharField(max_length=30, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	theatrical = models.BooleanField()
	website = models.URLField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('name',)

class Entry(models.Model):
	movie = models.ForeignKey(Movie, related_name='entries')
	date = models.DateField()
	venue = models.ForeignKey(Venue, related_name='entries', null=True, blank=True)
	format = models.CharField(max_length=1, choices=FORMATS, null=True, blank=True)
	in_3d = models.BooleanField(default=False)
	repeat = models.BooleanField(default=False)
	walkout = models.BooleanField(default=False)
	notes = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return "%s - %s " % (self.movie.title, self.date)

	class Meta:
		ordering = ('-pk',)
		verbose_name_plural = 'entries'

	@property
	def video(self):
		return not self.venue.theatrical
