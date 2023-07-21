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

#                                                  MAIN HOME PAGE VIEW
def index(request):
    # initializaiton of data
    all_teams = ""
    team_inputted = ""
    length_input = 0

    num_teams = len(Team.objects.all())

    # form processing for teams users are searching for
    if request.method == 'GET':
        team_inputted = request.GET.get('teamsearch')
        # this will only be true if team_inputted is not None or an empty string
        if (team_inputted and team_inputted != ""):
            length_input = len(team_inputted)
            # [0:5] splices the query set so we only see the first five filtered results
            all_teams = Team.objects.filter(name__icontains=team_inputted)[0:5]
        else:
            team_inputted = ""
    
    # generating context to be sent to the frontend
    context = {
        'all_teams': all_teams,
        'team_inputted': team_inputted,
        'length_input': length_input,
        'num_teams': num_teams,
    }
    # returning+rendering the template for the user
    return render(request,"portal/index.html", context)



#                                                               ADD USER INFORMATION POST GOOGLE LOGIN
def adduser(request):
    # after google login this will see if the user has already logged in. If they havent then we will begin to build a small default 
    # profile for the user that they can edit/add more stuff to on their own profile page
    try:
        # if the user has been created then just get it and do nothing
        user = User.objects.get(id=request.user.id, name=str(request.user.first_name + " " + request.user.last_name))
        return HttpResponseRedirect(reverse('index'))
    
    # if the user has not been created then create a default user and then return to index
    except:
        newUser = User(id=request.user.id, name=str(request.user.first_name + " " + request.user.last_name), year="", fav_throw="", 
                       role="", number=0, email=request.user.email, profile_img="", team="")
        newUser.save()
        return HttpResponseRedirect(reverse('index'))
    


#                                                                   ADD TEAM TO DATABASE VIEW
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
            level = request.POST.get("level")
            type = request.POST.get("type")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            # Make sure that all fields have been filled out
            if (name != "" and level != "" and type != "" and email != "" and password != "" and confirm_password != ""):
                if form.is_valid():
                    error_message = ""
                    # If both the password match and all the form has been filled out then the team is added to database
                    if (password == confirm_password):
                        error_message = ""
                        # Hashing passwords before storing them inside the database
                        hashed_pwd = make_password(password)
                        # check_password(password, hashed_pwd)
                        new_team = Team()
                        
                        # grab the cleaned data from the form. Store the hash of the password in the DB, and we only have the confirm password 
                        # so that users dont accidentally type the wrong password. We do not store the confirm password though
                        new_team.team_logo = form.cleaned_data['team_logo']
                        new_team.name = form.cleaned_data['name']
                        new_team.level = form.cleaned_data['level']
                        new_team.type = form.cleaned_data['type']
                        new_team.password = hashed_pwd
                        new_team.confirm_password = ""
                        new_team.email = form.cleaned_data['email']

                        new_team.save()

                        # after adding data to database redirect them to their own team portal
                        return HttpResponseRedirect(reverse('portal', args=(name,)))

                    # if the two passwords do not match then update the error message and display it so the user knows to fix these
                    else:
                        error_message = "The passwords do not match!"

            else:
                error_message = "Please fill out all of the fields before submitting!"
        
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


#                                                               HOME PORTAL FOR TEAMS VIEW
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


#                                                               SIGN INTO TEAM PORTAL VIEW
def team_login(request, name):
    # Initialization of data
    team = ""
    logged_in_msg = ""
    # get the first team with that name (if names are not unique we may need to process by IDs)
    team = Team.objects.filter(name=name).first()

    if (request.user.is_authenticated):
        logged_in_msg = ""
    
    else:
        logged_in_msg = "Before logging into your teams portal you must be signed in!"

    # generating context for the front end
    context = {
        'name': name,
        'team': team,
        'logged_in_msg': logged_in_msg,
    }

    return render(request, "portal/team_login.html", context)