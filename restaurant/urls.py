from django.urls import path
from django.conf import settings
from . import views

# Define URL patterns for the hw app
urlpatterns = [
    #path('', views.home, name="home"), 
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),
]