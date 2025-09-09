
from django.urls import path
from django.conf import settings
from . import views

# Define URL patterns for the hw app
urlpatterns = [
    #path('', views.home, name="home"), 
    path(r'', views.home_page, name="home"),
    path(r'about', views.about, name="about_page"),
]

