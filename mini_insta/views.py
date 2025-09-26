from django.shortcuts import render
from django.views.generic import ProfileListView, ProfileDetailView
from .models import Profile

# Create your views here.

class ShowAllView(ProfileListView):
    '''Define a view class to show all profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profile.html"
    context_object_name = "profiles"

class ProfileView(ProfileDetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/profile.html"
    context_object_name = "profile" 

