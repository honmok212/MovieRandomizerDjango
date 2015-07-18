from django.shortcuts import render
from django.http import HttpResponse
import random
import requests
import datetime
from django.utils import timezone

from .models import Movie

MOVIE_URL = "http://api.themoviedb.org/3/search/movie?api_key=14df543959099c2989514e3389387600&page=1&query="
POSTER_URL = "http://image.tmdb.org/t/p/w154"

def home(request):
    #remember to check for end of the week then delete all movies and refresh
    Movie.objects.all().delete()
    r = requests.get("https://www.kimonolabs.com/api/cbxx1jm4?apikey=0PYvN6gK4hT5I40kYSn0OQRiFJKDiPY4")
    rJson = r.json()
    for i in rJson['results']['collection1']:
        print len(rJson['results']['collection1'])
        print i
        movieName = i['movies']['text']
        print movieName
        movieWebsite = i['movies']['href']
        queryName = movieWebsite.split('/')
        print queryName
        print len(queryName)
        rInfo = requests.get(MOVIE_URL+queryName[len(queryName)-1] + "&year=" + str(timezone.now().year))
        print rInfo
        allInfo = rInfo.json()
        description = allInfo['results'][0]['overview']
        releaseDateStr = allInfo['results'][0]['release_date']
        releaseDate = datetime.datetime.strptime(releaseDateStr, "%Y-%m-%d")
        posterLink = POSTER_URL + str(allInfo['results'][0]['poster_path'])
        tempMovie = Movie(title = movieName, release_date = releaseDate, short_description = description, \
                          picture_url = posterLink, movie_url = movieWebsite)
        
        tempMovie.save()
        #c = Movie.objects.order_by('?').first()
    return HttpResponse("HI")

# Create your views here.
