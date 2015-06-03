from django.shortcuts import render
from django.http import HttpResponse
import random

from .models import Movie

def home(request):
	c = Movie.objects.order_by('?').first()
	return HttpResponse(c.title)

# Create your views here.
