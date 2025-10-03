# File: mini_insta/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines displays/views for the mini_insta app.

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Profile


# Create your views here.

class ProfileListView(ListView):
    '''Define a view class to show all profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profile.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" 

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

