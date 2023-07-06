from django.urls import path
from portal.views import index, addteam
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addteam/', views.addteam, name="addteam"),
    path('portal/<str:name>/', views.portal, name="portal"),
]