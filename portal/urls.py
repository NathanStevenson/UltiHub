from django.urls import path
from portal.views import index, addteam
from . import views

urlpatterns = [
    # The main page everyone lands on by default
    path('', views.index, name='index'),
    # Page to add your team to our database
    path('addteam/', views.addteam, name="addteam"),
    # Custom team portal that each team can customize
    path('portal/<str:name>/', views.portal, name="portal"),
    # Team Login to protect teams sensitive information
    path('<str:name>/login/', views.team_login, name="login"),
    # After google login redirected here so we can begin to build our profile for you
    path('adduser/', views.adduser, name="adduser"),
]