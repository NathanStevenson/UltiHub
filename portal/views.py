from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .models import *

# view for the main loading screen
def index(request):
    data = Team.objects.all()
    context = {
        'data' : data
    }
    return render(request,"index.html", context)