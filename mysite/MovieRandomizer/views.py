from django.shortcuts import render
from django.http import HttpResponse
import random
import requests
import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
from .models import Movie
import os

MOVIE_URL = "http://api.themoviedb.org/3/search/movie?api_key=14df543959099c2989514e3389387600&page=1&query="
POSTER_URL = "http://image.tmdb.org/t/p/w154"

MONTH_DICT = {"January":'1', "February":'2', "March":'3', "April":'4', "May":'5', "June":'6', "July":'7', "August":'8', "September":'9', "October":'10', "November":'11', "December":'12' }

def home(request):
#    #remember to check for end of the week then delete all movies and refresh
#    Movie.objects.all().delete()
#    r = requests.get("https://www.kimonolabs.com/api/cbxx1jm4?apikey=0PYvN6gK4hT5I40kYSn0OQRiFJKDiPY4")
#    rJson = r.json()
#    for i in rJson['results']['collection1']:
#        print len(rJson['results']['collection1'])
#        print i
#        movieName = i['movies']['text']
#        print movieName
#        movieWebsite = i['movies']['href']
#        queryName = movieWebsite.split('/')
#        print queryName
#        print len(queryName)
#        rInfo = requests.get(MOVIE_URL+queryName[len(queryName)-1] + "&year=" + str(timezone.now().year))
#        print rInfo
#        allInfo = rInfo.json()
#        description = allInfo['results'][0]['overview']
#        releaseDateStr = allInfo['results'][0]['release_date']
#        releaseDate = datetime.datetime.strptime(releaseDateStr, "%Y-%m-%d")
#        posterLink = POSTER_URL + str(allInfo['results'][0]['poster_path'])
#        tempMovie = Movie(title = movieName, release_date = releaseDate, short_description = description, \
#                          picture_url = posterLink, movie_url = movieWebsite)
#        
#        tempMovie.save()
#        #c = Movie.objects.order_by('?').first()
    if os.path.exists('getData.txt'):
        file = open('getData.txt', 'r')
        x = file.readline()
        file.close()
        newDate = x.split('-')
        print int(newDate[0])
        print newDate
        lastDate = datetime.datetime(int(newDate[0]), int(newDate[1]), int(newDate[2]))
        if ((datetime.datetime.now() - lastDate).days) >= 7:
            
            file = open('getData.txt', 'w')
            file.write(str(datetime.datetime.now().date()))
            Movie.objects.all().delete()
            getMovies()
            print "redid"
        else:
            print "did nothing"
    else:
        file = open('getData.txt', 'w')
        file.write(str(datetime.datetime.now().date()))
        Movie.objects.all().delete()
        getMovies()
        print "new"
    movies = Movie.objects.all()
    return render(request, 'MovieRandomizer/home.html', {'movies':movies})

# Create your views here.

def getMovies():
    url = "https://www.amctheatres.com"
    r = requests.get(url+"/movies")
    soup = BeautifulSoup(r.content)
    
    movies = soup.find_all("div", {"class":"thumbnail", "data-movie-released":"True"})
    
    for movie in movies:
        movieImg =  movie.contents[1].find_all("img")[0].get('src').strip()
        movieName =  movie.contents[3].text.strip()
        movieUrl =  url + movie.contents[3].find_all("a")[0].get('href').strip()
        #print movieImg
        #print movieName
        #print movieUrl
        newR = requests.get(movieUrl)
        s = BeautifulSoup(newR.content)
        movieDescr = s.find_all("p",{"itemprop":"description"})[0].text.strip()
        
        movieRelease = s.find_all("dd")
        movieRelease = movieRelease[len(movieRelease)-1].text.split()
        try:
            movieRelease[0]=MONTH_DICT[movieRelease[0]]
            movieRelease[1] = movieRelease[1].strip(',')
            movieRelease = ' '.join(movieRelease)
            releaseDate = datetime.datetime.strptime(movieRelease, "%m %d %Y")
        except KeyError:
            pass

        tempMovie = Movie(title = movieName, release_date = releaseDate, short_description = movieDescr, \
                          picture_url = movieImg, movie_url = movieUrl)
        tempMovie.save()

#print movieDescr

def getRandomMovie(request):
    randMovie = Movie.objects.order_by('?').first() # generate random Movie object
    context = {'randMovie': randMovie}
    return render(request, 'MovieRandomizer/rand.html', context)









