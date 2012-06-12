from django.db import models

GENDERS = (('M', 'Male'), ('F', 'Female'),)
FORMATS = (('0', '35mm'), ('1', 'DCP'), ('2', 'Blu-ray'), ('3', 'DVD'),
           ('4', 'HD Digital Download'), ('5', 'SD Digital Download'),
           ('6', 'HD Streaming'), ('7', 'SD Streaming'),
           ('8', 'HD Broadcast'),)
STARS = (('4', 'Masterpiece'), ('3', 'A Must See'), ('2', 'Average'),
         ('1', 'Poor'),)

class Director(models.Model):
	name = models.CharField(max_length=100, db_index=True)
	imdb = models.IntegerField()
	gender = models.CharField(max_length=1, choices=GENDERS)
	birth_year = models.CharField(max_length=4, null=True, blank=True)

class Movie(models.Model):
	title_sans_article = models.CharField(max_length=250, db_index=True)
	leading_article = models.CharField(max_length=3, null=True, blank=True)
	imdb = models.IntegerField()
	premiere_year = models.CharField(max_length=4)
	nyc_release_year = models.CharField(max_length=4, null=True, blank=True)
	directors = models.ManyToManyField(Director, related_name='movies')
	rating = models.IntegerField(null=True, blank=True)
	stars = models.CharField(max_length=1, choices=STARS, null=True, blank=True)

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

	class Meta:
		ordering = ('title_sans_article', 'leading_article', 'premiere_year',)

	def __unicode__(self):
		return self.title

class Venue(models.Model):
	name = models.CharField(max_length=100)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=2)
	theatrical = models.BooleanField()

class Entry(models.Model):
	movie = models.ForeignKey(Movie, related_name='entries')
	date = models.DateField()
	venue = models.ForeignKey(Venue, related_name='entries')
	format = models.CharField(max_length=1, choices=FORMATS)
	rating = models.IntegerField(null=True, blank=True)
	stars = models.CharField(max_length=1, choices=STARS, null=True, blank=True)

	@property
	def video(self):
		return not self.venue.theatrical

	def save(self, *args, **kwargs):
		s = super(Entry, self).save(*args, **kwargs)
		if self.rating:
			self.movie.rating = self.rating
		if self.stars:
			self.movie.stars = self.rating
		if self.rating or self.stars:
			self.movie.save()