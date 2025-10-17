# File: mini_insta/urls.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the URL patterns for the mini_insta app.

from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView
from .views import UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView
from .views import PostFeedListView

# Define URL patterns for the mini_insta app
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('show_all_profiles/', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path("profile/<int:pk>/create_post/", CreatePostView.as_view(), name="create_post"),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/feed', PostFeedListView.as_view(), name='show_feed'),
]

