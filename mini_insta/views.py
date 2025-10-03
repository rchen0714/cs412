# File: mini_insta/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines displays/views for the mini_insta app.

import profile
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from mini_insta.forms import CreatePostForm
from .models import Photo, Post, Profile


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


class CreatePostView(CreateView):
    '''Define a view class to create a new comment on an article'''

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Defines where to redirect the user after successfully creating
        a new post.'''

        pk = self.object.profile.pk
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
    def get_context_data(self):

        '''Defines and adds any extra context variables'''
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Called when a valid form is submitted.'''

        print(form.cleaned_data)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        form.instance.profile = profile

        response = super().form_valid(form)

        image_url = form.cleaned_data.get("image_url")
        if image_url:
            Photo.objects.create(post=self.object, image_url=image_url)

        return response
