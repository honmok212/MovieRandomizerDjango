from django.db import models

class Movie(models.Model):
	title = models.CharField(max_length=200)
    	release_date = models.DateTimeField('date published')
	short_description = models.CharField(max_length=500)
   	picture_url = models.CharField(max_length=100)
   	movie_url = models.CharField(max_length=100)
	#director = models.CharField(max_length=50)
	#genre = models.CharField(max_length=50)
	def __unicode__(self):
		return self.title

# Create your models here.
