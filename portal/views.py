from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from .models import *
from .forms import *

# to grab all of any model you can do: Model.objects.all() 
# if you just want to grab a subset you can do: Model.objects.filter() and then pass in arguments to filter by and ways you want to filter

# view for the main loading screen
def index(request):
    # initializaiton of data
    all_teams = ""

    # form processing for teams users are searching for
    if request.method == 'POST':
        team_inputted = request.POST.get('teamsearch', None)
        all_teams = Team.objects.filter(name__startswith=team_inputted)
    
    # generating context to be sent to the frontend
    context = {
        'all_teams': all_teams
    }
    print(all_teams)
    # returning+rendering the template for the user
    return render(request,"portal/index.html", context)



# view for adding new teams to our database
def addteam(request):
    # initialization of data
    error_message = ""
    # form processing for the new team
    if request.method == "POST":
        form = AddTeamForm(request.POST, request.FILES)

        # Logic for processing a new team (Eventually cross reference USAU, add model, redirect them to portal page)
        if request.POST.get("Submit"):
            print("Submitting")

            # getting the inputs from the form
            name = request.POST.get("name")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if form.is_valid():
                # This is how you get specific values from the Django Forms
                print(form.cleaned_data.get('name'))
                # If both the password match and all the form has been filled out then the team is added to database
                if (password == confirm_password):
                    error_message = ""
                    # Hashing passwords before storing them inside the database
                    hashed_pwd = make_password(password)
                    print(check_password(password, hashed_pwd))
                    
                    # add the team to the database by creating a class in Django
                    form.save()

                    # after adding data to database redirect them to their own team portal
                    return HttpResponseRedirect(reverse('portal', args=(name,)))

                # if the two passwords do not match then update the error message and display it so the user knows to fix these
                else:
                    error_message = "The passwords do not match!"
        
        # Logic for processing a cancelled form (Redirect them back to the default landing page)
        elif request.POST.get("Cancel"):
            print("Cancelling")
            # redirecting back to default landing page
            return HttpResponseRedirect(reverse('index'))
        
    else:
        form = AddTeamForm()

    # generating context for the front end
    context = {
        "error_message": error_message,
        "form": form,
    }

    # rendering the page for the user
    return render(request,"portal/addteam.html", context)


# this handles the backend logic for the portal main page
def portal(request, name):
    # initialization of the data
    team = ""
    # get the first team with that name (if names are not unique we may need to process by IDs)
    team = Team.objects.filter(name=name).first()
    print(team)
    # generating context for front end
    context = {
        'name': name,
        'team': team,
    }
    return render(request,"portal/portal.html", context)
