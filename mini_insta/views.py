# File: mini_insta/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines displays/views for the mini_insta app.

from importlib.resources import files
import profile
from .mixins import CheckLogin
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mini_insta.forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from .models import Photo, Post, Profile
from django.db.models import Q




# Create your views here.

class ProfileListView(ListView):
    '''Define a view class to show all profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profile.html"
    context_object_name = "profiles"

class ProfileDetailView(CheckLogin, DetailView):
    '''Display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile" 

    def get_object(self):
        '''Return the profile object for the currently logged-in user.'''
        if 'pk' in self.kwargs:
            return super().get_object()
        
        if self.request.user.is_authenticated:
            return self.get_my_profile()
        
        else:
            return None

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CheckLogin, CreateView):
    '''Define a view class to create a new comment on an article'''

    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Defines where to redirect the user after successfully creating
        a new post.'''

        pk = self.object.pk
        return reverse('show_post', kwargs={'pk': pk})
    
    def get_context_data(self, **kwargs):

        '''Defines and adds any extra context variables'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_my_profile()
        return context
    
    def form_valid(self, form):
        '''Called when a valid form is submitted.'''

        print(form.cleaned_data)

        post = form.save(commit=False)
        post.profile = self.get_my_profile()
        post.save()

        form.instance.profile = self.get_my_profile()

        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=post, image_file=file)
        
        response = super().form_valid(form)

        return response

class UpdateProfileView(CheckLogin, UpdateView):
    """Edit an already previously existing profile"""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        """Return the profile object for the currently logged-in user."""
        return self.get_my_profile()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["profile"] = post.profile 
        return context
    
    def get_success_url(self):
        """Redirect to the profile page of the updated profile."""
        return reverse('show_profile', kwargs={'pk': self.get_my_profile().pk})


class DeletePostView(CheckLogin, DeleteView):
    """Delete a post"""
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_queryset(self):
        """Limit deletion to posts owned by the logged-in user."""
        return Post.objects.filter(profile=self.get_my_profile())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context["post"] = post
        context["profile"] = post.profile 
        return context

    def get_success_url(self):
        """Redirect to the profile page of the deleted post."""
        return reverse('show_profile')

class UpdatePostView(CheckLogin, UpdateView):
    """Edit an already previously existing post"""
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_queryset(self):
        """Limit updates to posts owned by the logged-in user."""
        return Post.objects.filter(profile=self.get_my_profile())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context["post"] = post
        context["profile"] = post.profile 
        return context

    def get_success_url(self):
        """Redirect to the post page of the updated post."""
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
#Views for Following 

class ShowFollowersDetailView(DetailView):
    '''Display all followers of a profile'''

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    '''Display all profiles that a profile is following'''

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(CheckLogin, ListView):
    '''A view class that shows the post feed for a specific profile'''

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        '''Return the list of posts for this profile's feed'''

        profile = self.get_my_profile()
        feed = profile.get_post_feed()
        return feed
    
    def get_context_data(self, **kwargs):
        '''Defines and adds any extra context variables'''
        context = super().get_context_data(**kwargs)

        context['profile'] = self.get_my_profile()
        return context
    
class SearchView(CheckLogin, ListView):
    '''Search across specific profiles and posts based on a text query'''

    template_name = "mini_insta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''If no search query is provided, render the search page without results'''
        if 'q' not in self.request.GET:
            return render(request, "mini_insta/search.html", {"profile": self.get_my_profile()})

        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Return the list of profiles matching the search query'''

        query = self.request.GET.get('q', '')

        if not query:
            return Profile.objects.none()
        
        profiles = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        
        return profiles
    
    def get_context_data(self, **kwargs):
        '''returns a dictionary of all the context data from the template'''
        context = super().get_context_data(**kwargs)

        profile = self.get_my_profile()
        query = self.request.GET.get('q', '')

        if query:
             posts = Post.objects.filter(caption__icontains=query).order_by('-timestamp')
        else: 
             posts = Post.objects.none()
        
        profiles = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )

        context['profile'] = profile
        context['profiles'] = profiles
        context['posts'] = posts
        context['query'] = query

        return context


