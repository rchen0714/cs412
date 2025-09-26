# File: mini_insta/urls.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the URL patterns for the mini_insta app.

from django.urls import path
from .views import ProfileListView, ProfileDetailView

# Define URL patterns for the mini_insta app
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('show_all_profiles/', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
]