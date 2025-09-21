# File: restaurant/urls.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the URL patterns for the restaurant app.

from django.urls import path
from django.conf import settings
from . import views

# Define URL patterns for the hw app
urlpatterns = [
    #path('', views.home, name="home"), 
    path(r'', views.main, name="main_page"),
    path(r'main', views.main, name="main_page"),
    path(r'order', views.order, name="order_page"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]