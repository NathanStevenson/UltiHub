from django.urls import path
from portal.views import index
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]