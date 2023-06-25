from django.shortcuts import render, redirect
from django.contrib.auth import logout
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
    return render(request,"portal/index.html", context)
