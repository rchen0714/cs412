# File: mini_insta/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines displays/views for the mini_insta app.

from importlib.resources import files
import profile
from .mixins import CheckLogin
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from mini_insta.forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from .models import Follow, Like, Photo, Post, Profile
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
        
    def get_context_data(self, **kwargs):

        #use the super method to get the existing context
        context = super().get_context_data(**kwargs)

        #add the current profile instance 
        context['profile'] = self.get_object()

        # If logged in, check whether the user is following the target profile
        if self.request.user.is_authenticated:
            user = self.get_my_profile()
            target_profile = self.object
            context['is_following'] = user.check_following(target_profile)
        else: 
            context['is_following'] = False

        return context

class PostDetailView(DetailView):
    '''Display a single post'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):

        #use the super method to get the existing context
        context = super().get_context_data(**kwargs)

        # If logged in, check whether the user has liked the post
        if self.request.user.is_authenticated:
            user = Profile.objects.get(user=self.request.user)
            context['is_liked'] = self.object.check_liked_by(user)
        else: 
            context['is_liked'] = False

        return context


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
        context['profile'] = self.get_my_profile()
        return context
    
    def get_success_url(self):
        """Redirect to the profile page of the updated profile."""
        profile = self.get_my_profile()
        return reverse('show_profile', kwargs={'pk': profile.pk})


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
        post = self.get_object()
        profile = post.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})

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
    

class CreateProfileView(CreateView):
    """Create a new profile for a user"""

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''Called when a valid form is submitted.'''

        # create a new user account using djangos built-in method 
        user_form = UserCreationForm(self.request.POST)
        
        # if the user is valid, save the user and log them in
        if user_form.is_valid():
            user = user_form.save()
        else:
            # if the user form is not valid, re-render the page with error messages
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

        # log the user in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # connect the new profile with the newly created user
        form.instance.user = user

        # save the profile instance
        response = super().form_valid(form)

        return response
    
    def get_success_url(self):
        """Redirect to the profile page of the created profile."""

        profile = self.object
        return reverse('show_profile', kwargs={'pk': profile.pk})


class FollowView(CheckLogin, TemplateView):
    """Allows a logged-in user to follow a target profile. Also double checks
    that the user is logged in before allowing them to follow another profile."""

    def dispatch(self, request, *args, **kwargs):
        
        #checks the authentication of the user. If the user is not logged in, 
        #redirect them to the login page.

        if not request.user.is_authenticated:
            return redirect('login')
        
        # Retrieve the Profile object of the logged-in user
        # and the target profile to be followed.

        pk = self.kwargs['pk']
        follower = self.get_my_profile()
        target_profile = get_object_or_404(Profile, pk=pk)

        # Prevent users from following themselves
        if target_profile != follower: 

            # Create a follow relationship
            Follow.objects.get_or_create(
                profile=target_profile,
                follower_profile=follower
            )
        #redirect back to the target profile page afterwards 
        return redirect('show_profile', pk=target_profile.pk)
    
class UnfollowView(CheckLogin, TemplateView):
    """Allows a logged-in user to unfollow a target profile. 
    Also double checks that the user is logged in before allowing them to unfollow another profile."""

    def dispatch(self, request, *args, **kwargs):
        
        #checks the authentication of the user. If the user is not logged in, 
        #redirect them to the login page.

        if not request.user.is_authenticated:
            return redirect('login')
        
        # retrieve the Profile object of the logged-in user
        # and the target profile to be unfollowed.

        pk = self.kwargs['pk']
        follower = self.get_my_profile()
        target_profile = get_object_or_404(Profile, pk=pk)

        # prevent users from unfollowing themselves
        # remove any follow relationship that matches both users
        
        Follow.objects.filter(
            profile=target_profile,
            follower_profile=follower
        ).delete()

        #redirect back to the target profile page afterwards 
        return redirect('show_profile', pk=target_profile.pk)
    
class LikePostView(CheckLogin, TemplateView):
    """Allows a logged-in user to like a post."""

    def dispatch(self, request, *args, **kwargs):

        # retrieve the Profile object of the logged-in user
        # and the target post to be liked.

        pk = self.kwargs['pk']
        profile = self.get_my_profile()
        post = get_object_or_404(Post, pk=pk)

        # prevent users from liking their own posts
        if post.profile != profile:
            # create a like relationship
            Like.objects.get_or_create(
                post=post,
                profile=profile
            )

        # redirect back to the post afterwards
        return redirect('show_post', pk=post.pk)
    

class UnlikePostView(CheckLogin, TemplateView):
    """Allows a logged-in user to unlike a post."""

    def dispatch(self, request, *args, **kwargs):

        # retrieve the Profile object of the logged-in user
        # and the target post to be unliked.

        pk = self.kwargs['pk']
        profile = self.get_my_profile()
        post = get_object_or_404(Post, pk=pk)

        # remove any like relationship that matches both the user and the post
        Like.objects.filter(
            post=post,
            profile=profile
        ).delete()

        # redirect back to the post afterwards
        return redirect('show_post', pk=post.pk)



