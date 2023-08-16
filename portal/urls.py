from django.urls import path
from portal.views import index, addteam
from . import views

urlpatterns = [
    # MISC ROUTES
    # The main page everyone lands on by default
    path('', views.index, name='index'),
    # Page to add your team to our database
    path('addteam/', views.addteam, name="addteam"),
    # After google login redirected here so we can begin to build our profile for you
    path('adduser/', views.adduser, name="adduser"),

    # PORTAL ROUTES
    # Custom team portal that each team can customize
    path('portal/<str:name>/', views.portal, name="portal"),
    # Team Login to protect teams sensitive information
    path('<str:name>/login/', views.team_login, name="login"),
    # allows teams to add their custom events to their portal
    path('portal/<str:name>/addevent/', views.add_event, name="add_event"),
    # this route is only available to users who have admin privileges
    path('portal/<str:name>/admin/', views.admin_page, name="admin_page"),

    # GRANTING/REMOVING PERMISSIONS
    path('portal/<str:name>/grant_admin/<int:userID>/', views.grant_admin, name="grant_admin"),
    path('portal/<str:name>/remove_admin/<int:userID>/', views.remove_admin, name="remove_admin"),
    path('portal/<str:name>/search_player/', views.search_player, name='search_player'),
    path('portal/<str:name>/add_player/<int:userID>/', views.add_player, name='add_player'),
    path('portal/<str:name>/remove_player/<int:userID>/', views.remove_player, name='remove_player'),

    # DROPDOWN MENU ROUTES
    # displays profile information about a current user
    path('profile/', views.profile, name="profile"),
    # allows users to edit/add details to their user profile
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    # route to our contact menu to allow you to tell us about bugs or any new features
    path('contact/', views.contact, name='contact'),
    # route to our about page, describe myself and the goal of the website
    path('about/', views.about, name='about'), 
]