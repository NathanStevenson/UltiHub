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

                # Make sure that all fields have been filled out
                if (name != "" and level != "" and type != "" and email != ""):
                    if form.is_valid():
                        error_message = ""
                        new_team = Team()
                        
                        # grab the cleaned data from the form. Store the hash of the password in the DB, and we only have the confirm password 
                        # so that users dont accidentally type the wrong password. We do not store the confirm password though
                        new_team.team_logo = form.cleaned_data['team_logo']
                        new_team.name = form.cleaned_data['name']
                        new_team.level = form.cleaned_data['level']
                        new_team.type = form.cleaned_data['type']
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
    team_admin = team.admin.all()

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
                'name': name,
                'team_admin': team_admin,
            }
            return render(request,"portal/unauthorized.html", context)
    
    # If not autheticated send them to error page stating that they need to sign in in order to continue
    if (not request.user.is_authenticated):
        context = {}
        return render(request, "portal/signin.html", context)


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
            # generate a list of all current players and admin to pass to the front end
            team_players = team.players.all()
            team_admin = team.admin.all()
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
                'team_players': team_players,
                'team_admin': team_admin,
            }
            return render(request, 'portal/admin_page.html', context)

        # if the user is not allowed then send them to unauthorized page
        else:
            context = {
                'team_admin': team_admin,
            }
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


#                                                   GRANTING USER PERMISSIONS VIEWS

# add security to this to make sure you cant just remove random ppl from the site

# Giving admin permissions to a team member for the portal
def grant_admin(request, name, userID):
    # get the current team
    team = Team.objects.get(name=name)
    team_admin = team.admin.all()
    # make sure the user has signed in
    if request.user.is_authenticated:
        # make sure the user is allowed to access the team and has admin privileges to add/remove
        activeUserID = request.user.id
        activeUser = User.objects.get(id=activeUserID)
        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # figure out whether the user is an admin or not
        is_admin = activeUser in team.admin.all()

        # if the user is a part of the team and is also an admin they can add players
        if user_allowed and is_admin:
            team = Team.objects.get(name=name)
            playerAdded = User.objects.get(id=userID)

            team.admin.add(playerAdded)

            return HttpResponseRedirect(reverse('admin_page', args=(name,)))
        
        # if the user does not have the proper permissions
        else:
            context = {
                'team_admin': team_admin,
            }
            return render(request, 'portal/unauthorized.html', context)
    
    # if the user has not signed into their account
    else:
        context = {}
        return render(request, 'portal/signin.html', context)

# removing admin permissions for a team memeber for the portal
def remove_admin(request, name, userID):
    # get the current team
    team = Team.objects.get(name=name)
    team_admin = team.admin.all()
    # make sure the user has signed in
    if request.user.is_authenticated:
        # make sure the user is allowed to access the team and has admin privileges to add/remove
        activeUserID = request.user.id
        activeUser = User.objects.get(id=activeUserID)
        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # figure out whether the user is an admin or not
        is_admin = activeUser in team.admin.all()

        # if the user is a part of the team and is also an admin they can add players
        if user_allowed and is_admin:
            team = Team.objects.get(name=name)
            playerAdded = User.objects.get(id=userID)

            team.admin.remove(playerAdded)

            return HttpResponseRedirect(reverse('admin_page', args=(name,)))
        
        # if the user does not have the proper permissions
        else:
            context = {
                'team_admin': team_admin,
            }
            return render(request, 'portal/unauthorized.html', context)
    
    # if the user has not signed into their account
    else:
        context = {}
        return render(request, 'portal/signin.html', context)

# search for your teammate to add to the portal
def search_player(request, name):
    team = Team.objects.get(name=name)
    # this generates a list of user IDs who are already a member of your team
    team_players_id = team.players.all().values_list('id', flat=True)
    team_admin = team.admin.all()

    # if the user has logged into their google account
    if request.user.is_authenticated:
        # get the userID of the current user
        userID = request.user.id
        activeUser = User.objects.get(id=userID)
        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # figure out whether the user is an admin or not
        is_admin = activeUser in team.admin.all()

        # if the user is a part of the team and is also an admin they can add players
        if user_allowed and is_admin:
            # initializaiton of data
            all_players = ""
            player_inputted = ""
            length_input = 0

            # form processing for teams users are searching for
            if request.method == 'GET':
                player_inputted = request.GET.get('player_search')
                # this will only be true if team_inputted is not None or an empty string
                if (player_inputted and player_inputted != ""):
                    length_input = len(player_inputted)
                    # [0:5] splices the query set so we only see the first five filtered results
                    # excludes all players already inside of your team
                    all_players = User.objects.filter(name__icontains=player_inputted).exclude(id__in=team_players_id)[0:5]
                else:
                    player_inputted = ""

            # generating context for the front end
            context = {
                'is_admin': is_admin,
                'all_players': all_players,
                'player_inputted': player_inputted,
                'length_input': length_input,
                'name': name,
            }
            return render(request, 'portal/search_player.html', context)
        
        # if they are not an admin
        else:
            context = {
                'team_admin': team_admin,
            }
            return render(request, 'portal/unauthorized.html', context)

    # if the user has not logged into their google account have them sign in
    else:
        context = {}
        return render(request, 'portal/signin.html')


# adding a new player to the portal (the new login method)
def add_player(request, name, userID):
    # get the current team
    team = Team.objects.get(name=name)
    team_admin = team.admin.all()
    # make sure the user has signed in
    if request.user.is_authenticated:
        # make sure the user is allowed to access the team and has admin privileges to add/remove
        activeUserID = request.user.id
        activeUser = User.objects.get(id=activeUserID)
        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # figure out whether the user is an admin or not
        is_admin = activeUser in team.admin.all()

        # if the user is a part of the team and is also an admin they can add players
        if user_allowed and is_admin:
            team = Team.objects.get(name=name)
            playerAdded = User.objects.get(id=userID)

            # add the chosen player to the team and then team to the chosen player
            team.players.add(playerAdded)
            playerAdded.teams_allowed.add(team)

            return HttpResponseRedirect(reverse('search_player', args=(name,)))
        
        # if the user does not have the proper permissions
        else:
            context = {
                'team_admin': team_admin,
            }
            return render(request, 'portal/unauthorized.html', context)
    
    # if the user has not signed into their account
    else:
        context = {}
        return render(request, 'portal/signin.html', context)

# removing a player from the portal
def remove_player(request, name, userID):
    # get the current team
    team = Team.objects.get(name=name)
    team_admin = team.admin.all()
    # make sure the user has signed in
    if request.user.is_authenticated:
        # make sure the user is allowed to access the team and has admin privileges to add/remove
        activeUserID = request.user.id
        activeUser = User.objects.get(id=activeUserID)
        # call this to determine if the user is allowed to view sensitive team info
        user_allowed = helper_isauthorized(request, team)
        # figure out whether the user is an admin or not
        is_admin = activeUser in team.admin.all()

        # if the user is a part of the team and is also an admin they can add players
        if user_allowed and is_admin:
            team = Team.objects.get(name=name)
            playerAdded = User.objects.get(id=userID)

            team.players.remove(playerAdded)

            return HttpResponseRedirect(reverse('admin_page', args=(name,)))
        
        # if the user does not have the proper permissions
        else:
            context = {
                'team_admin': team_admin,
            }
            return render(request, 'portal/unauthorized.html', context)
    
    # if the user has not signed into their account
    else:
        context = {}
        return render(request, 'portal/signin.html', context)


#                                                                               HELPER FUNCTIONS
def helper_isauthorized(request, team):
    # this function takes a request and a given team name and returns a bool to decide whether the user can view
    userID = request.user.id
    activeUser = User.objects.get(id=userID)
    active_team = Team.objects.get(name=team)

    # see if the user making the request is in the players allowed for the given team
    user_allowed = (activeUser in active_team.players.all())

    return user_allowed