from django.db import models

from filmlog.managers import EntryManager

# Most of these are pretty clear. DCP is inclusive of any digital format presented at a DCP-capable venue (since usually they're upconverting even if the source material is HDCAM or Blu-ray). Broadcast/VOD basically just means anything I've watched on TV via my cable provider.
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

	@property
	def directors_as_str(self):
		directors = self.directors.all()
		if directors.count() == 0:
			return ''
		if directors.count() == 1:
			return directors[0].name
		all = list(directors.values_list('name', flat=True))
		last = all.pop(-1)
		return "%s & %s" % (", ".join(all), last)

	@property
	def versions(self):
		return self.entries.values_list('version', flat=True)

	@property
	def seen(self):
		if self.entries.exclude(walkout=True).count() > 0:
			return True
		return False

	@property
	def last_seen(self):
		if self.seen:
			return self.entries.filter(walkout=False).order_by('-pk')[0]
		return None

	@property
	def recommended(self):
		return self.last_seen.recommended

	@property
	def great(self):
		return self.last_seen.great

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

def only_walkouts_prior_to_entry(obj):
	if obj.repeat:
		if obj.movie.pk not in Entry.objects.walkout_list:
			return False
		qs = Entry.objects.filter(movie=obj.movie, date__lte=obj.date).exclude(id=obj.id)
		if qs.count() > 0:
			if qs.filter(walkout=True).count() == qs.count():
				return True
	return False

class Entry(models.Model):
	movie = models.ForeignKey(Movie, related_name='entries')
	date = models.DateField()
	venue = models.ForeignKey(Venue, related_name='entries', null=True, blank=True)
	format = models.CharField(max_length=1, choices=FORMATS, null=True, blank=True)
	in_3d = models.BooleanField(default=False, verbose_name='3d')
	repeat = models.BooleanField(default=False, verbose_name='//')
	walkout = models.BooleanField(default=False, verbose_name='W')
	notes = models.TextField(blank=True, null=True)
	recommended = models.BooleanField(default=False, verbose_name='+')
	great = models.BooleanField(default=False, verbose_name='G')
	version = models.CharField(max_length=50, null=True, blank=True)

	objects = EntryManager()

	def __unicode__(self):
		return "%s - %s " % (self.movie.title, self.date)

	class Meta:
		ordering = ('pk',)
		verbose_name_plural = 'entries'

	def save(self, *args, **kwargs):
		if self.great:
			self.recommended = True
		if self.walkout or not self.recommended:
			self.great = False
		if self.walkout:
			self.recommended = False
		return super(Entry, self).save(*args, **kwargs)

	@property
	def video(self):
		return not self.venue or not self.venue.city

	@property
	def reverse_slashes(self):
		return only_walkouts_prior_to_entry(self)

	@property
	def special_format(self):
		flag = ''
		if not self.video:
			if self.format == '0':
				flag = '35mm'
			elif self.format == 'L':
				flag = 'Digital IMAX'
			elif self.format == 'I':
				flag = '70mm IMAX'
			elif self.format == 'S':
				flag = '70mm'
			else:
				flag = 'Digital'
			if self.in_3d:
				flag += ' 3-D'
		return flag.strip()
