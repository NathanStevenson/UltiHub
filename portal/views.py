from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
import datetime
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
        user = User.objects.get(id=request.user.id)
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
    # user must be logged into their account to add a team because they become the first admin
    if request.user.is_authenticated:
        # gather the user who is creating the account so that we can make them team admin
        userID = request.user.id
        activeUser = User.objects.get(id=userID)
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


                            # add the two default options to the teams upon login (team logistics and practice plans)
                            team_logistics = portalOptions.objects.get(name="Logistics")
                            practice_plans = portalOptions.objects.get(name="Practice Plans")
                            # if we want to add more default options to the portal in the future we can do that here
                            new_team.portal_options.add(team_logistics)
                            new_team.portal_options.add(practice_plans)

                            # add the new user to the admin and player fields for the new team
                            new_team.players.add(activeUser)
                            new_team.admin.add(activeUser)
                            activeUser.teams_allowed.add(new_team)

                            # after adding data to database redirect them to their teams login page so they can access their newly created team
                            return HttpResponseRedirect(reverse('login', args=(name,)))

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
    
    # else if not logged in then send them to the sign in page
    else:
        context = {}
        return render(request,"portal/signin.html", context)



#                                                              DISPLAY PROFILE INFO VIEW
def profile(request):
    # account for whether or not the user is authenticated so we know who they are
    if request.user.is_authenticated:
        user_id = request.user.id
        activeUser = User.objects.get(id=user_id)
        # account for whether the user is already logged into a team portal or not so we know what the navbar should display

        # generating context for front-end
        context = {
            'activeUser': activeUser,
        }
        return render(request,"portal/profile.html", context)

    # the user is not logged into anything and is trying to access their profile
    else:
        context = {}
        return render(request, 'portal/signin.html', context)


#                                                                EDIT PROFILE INFO VIEW
def edit_profile(request):
    # initialization of data
    form = UserInfoForm()
    error_msg = ""

    # if the user has logged in
    if request.user.is_authenticated:
        userID = request.user.id
        activeUser = User.objects.get(id=userID)
        form = UserInfoForm(instance=activeUser)

        if request.method == "POST":
            if request.POST.get("Submit"):
                # get the values upon submission
                name = request.POST.get("name")
                year = request.POST.get("year")
                fav_throw = request.POST.get("fav_throw")
                email = request.POST.get("email")
                number = request.POST.get("number")
                team = request.POST.get("team")

                form = UserInfoForm(request.POST, request.FILES)
                if form.is_valid():
                    if name != "" and year != "" and fav_throw != "" and email != "" and number != "" and team != "":
                        error_msg = ""

                        activeUser.name = form.cleaned_data['name']
                        activeUser.year = form.cleaned_data['year']
                        activeUser.fav_throw = form.cleaned_data['fav_throw']
                        activeUser.email = form.cleaned_data['email']
                        activeUser.number = form.cleaned_data['number']
                        activeUser.team = form.cleaned_data['team']

                        # if the user uploads a new profile image then change it
                        if form.cleaned_data['profile_img']:
                            print('here')
                            activeUser.profile_img = form.cleaned_data['profile_img']

                        # otherwise keep the profile image the same

                        activeUser.save()

                        # send the user back to their profile
                        return HttpResponseRedirect(reverse('profile'))

                    else:
                        error_msg = "All fields must be filled out"

            # if cancel is hit take them back to where they came from (index for rn) 
            elif request.POST.get("Cancel"):
                return HttpResponseRedirect(reverse('index'))


        # generating context for front-end
        context = {
            'form': form,
            'activeUser': activeUser,
            'error_message': error_msg,
        }
        return render(request,"portal/edit_profile.html", context)
    
    # if the user has not logged in then send them to the sign in page
    else:
        context = {}
        return render(request, 'portal/signin.html', context)

#                                                               HOME PORTAL FOR TEAMS VIEW
def portal(request, name):
    # initialization of the data
    team = ""
    team_events = ""
    team = Team.objects.get(name=name)

    # get the current date and parse it into day/month/year
    today = str(datetime.date.today())
    today = today.split("-")
    day = today[2]
    month = today[1]
    year = today[0]
    team_events = team.team_events.all()

    # User must be authenticated to log into their team portal so we know who they are
    if request.user.is_authenticated:
        # figure out who the active user is
        userID = request.user.id
        activeUser = User.objects.get(id=userID)
        # determine whether the user is an admin of the current team
        is_admin = activeUser in team.admin.all()

        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # if the user is allowed to view this team
        if user_allowed:       
            # generating context for front end
            context = {
                'name': name,
                'team': team,
                'day': day,
                'month': month,
                'year': year,
                'team_events': team_events,
                'is_admin': is_admin,
            }
            return render(request,"portal/portal.html", context)
        
        # if the user is not allowed
        if (not user_allowed):
            context = {
                'name':name,
            }

            return render(request,"portal/unauthorized.html", context)
    
    # If not autheticated send them to error page stating that they need to sign in in order to continue
    if (not request.user.is_authenticated):

        context = {

        }

        return render(request, "portal/signin.html", context)


#                                                               SIGN INTO TEAM PORTAL VIEW
def team_login(request, name):
    # Initialization of data
    team = ""
    logged_in_msg = ""
    wrong_password = ""
    # get the first team with that name (if names are not unique we may need to process by IDs)
    team = Team.objects.filter(name=name).first()

    if (request.user.is_authenticated):
        logged_in_msg = ""
        wrong_password = ""
        # grab the user who is currently using the site so after logging in we can successfully add that team to their allowed teams so no more logging in
        userID = request.user.id
        activeUser = User.objects.get(id=userID)

        # if this user has already signed in before and they have been allowed to view the team then just redirect them to the teams portal to simplify login
        is_authorized = helper_isauthorized(request, team)
        if is_authorized:
            return HttpResponseRedirect(reverse('portal', args=(name,)))

        # on form submission
        if request.method == "POST":
            # if the user is submitting the form then process the username and password and then redirect if password is right
            if request.POST.get("Submit"):
                username = request.POST.get("username")
                password = request.POST.get("password")

                # update the users username if they choose to be called something else when entering the portal
                user = User.objects.get(id=request.user.id)
                user.name = username
                user.save()

                # check if the password the user inputted is the same as the hashed teams password
                hashed_pwd = team.password
                matches = check_password(password, hashed_pwd)
                
                # if password matches then take the user to their portal
                if matches:
                    # log in will be complete once we add a step where user is authorized to view the team
                    team.players.add(activeUser)
                    # add the team to the teams allowed for the user for quick access
                    activeUser.teams_allowed.add(team)

                    return HttpResponseRedirect(reverse('portal', args=(name,)))
                
                else:
                    wrong_password = "Password does not match."


            # if the user is cancelling the form then redirect them back to the index page to continue their search
            if request.POST.get("Cancel"):
                return HttpResponseRedirect(reverse('index'))
    
    else:
        logged_in_msg = "Before logging into your teams portal you must be signed in!"

    # generating context for the front end
    context = {
        'name': name,
        'team': team,
        'logged_in_msg': logged_in_msg,
        'wrong_password': wrong_password,
    }

    return render(request, "portal/team_login.html", context)


#                                                     ADMIN PAGE THAT HAS CUSTOMIZING OPTIONS + PRIVILEGES
def admin_page(request, name):
    # get the team name
    team = Team.objects.get(name=name)

    # user must be logged in else send them to sign in page
    if request.user.is_authenticated:
        # get the userID of the current user
        userID = request.user.id
        activeUser = User.objects.get(id=userID)
        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # figure out whether the user is an admin or not
        is_admin = activeUser in team.admin.all()
      
        # if the user is allowed
        if user_allowed and is_admin:
            # all of the potential values of the Events: "Discussion Board", "Logistics", "Film Room", "Practice Plans"
            # figure out which options have been checked
            current_options = team.portal_options.all()

            # setting up to see which events have been checked off
            db_object = portalOptions.objects.get(name="Discussion Board")
            log_object = portalOptions.objects.get(name="Logistics")
            fr_object = portalOptions.objects.get(name="Film Room")
            pp_object = portalOptions.objects.get(name="Practice Plans")

            # checking which values are active
            is_db = db_object in current_options
            is_log = log_object in current_options
            is_fr = fr_object in current_options
            is_pp = pp_object in current_options

            # upon the form submission update the teams portal options
            if request.method == "POST":

                # LOGISTICS
                # if logistics is checked and not added to the team log then add it
                if request.POST.get("logistics") and not is_log:
                    team.portal_options.add(log_object)

                # if they unclick the box and logistics is in the team options then remove it
                if not request.POST.get("logistics") and is_log:
                    team.portal_options.remove(log_object)

                # PRACTICE PLANS

                # if practice is checked and not added to the team log then add it
                if request.POST.get("practice") and not is_pp:
                    team.portal_options.add(pp_object)

                # if they unclick the box and practice is in the team options then remove it
                if not request.POST.get("practice") and is_pp:
                    team.portal_options.remove(pp_object)

                # DISCUSSION BOARD

                # if discussion is checked and not added to the team log then add it
                if request.POST.get("discussion") and not is_db:
                    team.portal_options.add(db_object)

                # if they unclick the box and discussion boards is in the team options then remove it
                if not request.POST.get("discussion") and is_db:
                    team.portal_options.remove(db_object)

                # FILM ROOM

                # if film is checked and not added to the team log then add it
                if request.POST.get("film") and not is_fr:
                    team.portal_options.add(fr_object)

                # if they unclick the box and logistics is in the team options then remove it
                if not request.POST.get("film") and is_fr:
                    team.portal_options.remove(fr_object)
                

                # updating the values for the checkbox
                current_options = team.portal_options.all()
                is_db = db_object in current_options
                is_log = log_object in current_options
                is_fr = fr_object in current_options
                is_pp = pp_object in current_options


            # context to pass to the front end
            context = {
                'is_admin': is_admin,
                'is_db': is_db,
                'is_log': is_log,
                'is_fr': is_fr,
                'is_pp': is_pp,
                'name': name,
            }
            return render(request, 'portal/admin_page.html', context)

        # if the user is not allowed then send them to unauthorized page
        else:
            context = {}
            return render(request, 'portal/unauthorized.html', context)
    
    # if user has not logged in then send them to sign in page
    else:
        context = {}
        return render(request, 'portal/signin.html', context)

#                                                                      ADDING UPCOMING TEAM EVENTS VIEW
def add_event(request, name):
    # initializing all data
    form = addEventForm()
    error_message = ""

    # processing logic
    if request.method == "POST":
        # if the form is being submitted
        if request.POST.get("Submit"):
            # set the form to have the current POST data
            form = AddTeamForm(request.POST)
            # getting the form inputs
            date = request.POST.get('date')
            event_name = request.POST.get('event_name')
            notes = request.POST.get('notes')
            # make sure none of the values are blank if they are then update error message
            if (date != "" and event_name != "" and notes != ""):
                # if the form is valid then save it and send the user back to their portal page
                error_message = ""
                if form.is_valid():
                    newEvent = Event(date=date, event_name=event_name, notes=notes)
                    newEvent.save()
                    team = Team.objects.get(name=name)
                    team.team_events.add(newEvent)
                    return HttpResponseRedirect(reverse('portal', args=(name,)))
            # if any of the fields have a blank value
            else:
                error_message = "One of your fields is blank. Please fill out all fields!"

        # if the form is cancelled then send the user back to their portal page
        elif request.POST.get("Cancel"):
            return HttpResponseRedirect(reverse('portal', args=(name,)))


    # generating context for the front end
    context = {
        'form': form,
        'error_message': error_message,
    }

    return render(request, "portal/add_event.html", context)


#                                                           CONTACT VIEW PAGE
def contact(request):

    context = {}
    return render(request, 'portal/contact.html', context)


#                                                           ABOUT VIEW PAGE
def about(request):
    
    context = {}
    return render(request, 'portal/about.html', context)


#                                                                               HELPER FUNCTIONS
def helper_isauthorized(request, team):
    # this function takes a request and a given team name and returns a bool to decide whether the user can view
    userID = request.user.id
    activeUser = User.objects.get(id=userID)
    active_team = Team.objects.get(name=team)

    # see if the user making the request is in the players allowed for the given team
    user_allowed = (activeUser in active_team.players.all())

    return user_allowed