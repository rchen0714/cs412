# File: mini_insta/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines displays/views for the mini_insta app.

from importlib.resources import files
import profile
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mini_insta.forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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
        return reverse('show_post', kwargs={'pk': pk})
    
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

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        form.instance.profile = profile

        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=post, image_file=file)
        response = super().form_valid(form)

        return response
    
class UpdateProfileView(UpdateView):
    """Edit an already previously existing profile"""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"


class DeletePostView(DeleteView):
    """Delete a post"""
    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Provide post and profile to the template."""
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        context["post"] = post
        context['profile'] = post.profile

        return context

    def get_success_url(self):
        """Redirect to the profile page of the deleted post."""
        post = self.get_object()
        return reverse('show_profile', kwargs={'pk': post.profile.pk})
    
class UpdatePostView(UpdateView):
    """Edit an already previously existing post"""
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        """Provide post and profile to the template."""
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        context["post"] = post
        context['profile'] = post.profile

        return context

    def get_success_url(self):
        """Redirect to the post page of the updated post."""
        post = self.get_object()
        return reverse('show_post', kwargs={'pk': post.pk})

    

