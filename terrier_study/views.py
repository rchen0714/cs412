
# File: terrier_study/views.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This is all the views for the terrierstudy application


from django.shortcuts import render
from importlib.resources import files
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login 

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from cs412 import settings
from .mixins import CheckLogin
from .forms import *

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

import random

from .models import * 
from .serializer import *


class BuildingListView(ListView):
    """View that showsw all buildings."""
    model = Building
    template_name = "terrier_study/building_list.html"
    context_object_name = "buildings"

class BuildingDetailView(DetailView):
    """DetailView that shows a single building and its study rooms."""
    model = Building
    template_name = "terrier_study/building_detail.html"
    context_object_name = "building"

    def get_context_data(self, **kwargs):
        """add a study rooms context data"""
        context = super().get_context_data(**kwargs)
        building = self.object
        context["rooms"] = building.study_rooms.all()
        return context
    
class StudyRoomListView(ListView):
    """View that shows all study rooms with optional filtering."""
    model = StudyRoom
    template_name = "terrier_study/studyroom_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = StudyRoom.objects.all()

        # grab the FK building 
        building_id = self.request.GET.get("building")
        if building_id:
            queryset = queryset.filter(building__id=building_id)

        #filter the features by the model boolean inputs
        for feature in ["on_campus", "id_required", "wifi", "outlets", "windows", "whiteboard"]:
            val = self.request.GET.get(feature)
            if val == "true":
                queryset = queryset.filter(**{feature: True})
            elif val == "false":
                queryset = queryset.filter(**{feature: False})

        return queryset

    def get_context_data(self, **kwargs):
        """return context data including buildings for dropdown"""
        context = super().get_context_data(**kwargs)
        context["buildings"] = Building.objects.all()  # needed for dropdown
        return context

class CreateStudyRoomView(CheckLogin, CreateView):
    """Allows a logged-in user to create a new study room."""

    model = StudyRoom
    form_class = CreateStudyRoomForm
    template_name = "terrier_study/create_studyroom_form.html"

    def form_valid(self, form):
        """Used to check whether a valid form is submitted."""
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the detail page of the newly created study room."""
        #grab the room id and do a reverse search of the primary key
        room_id = self.object.pk
        return reverse("studyroom-detail", kwargs={"pk": room_id})

    def get_context_data(self, **kwargs):
        """Add any needed context variables."""
        context = super().get_context_data(**kwargs)
        
        return context
    
class StudyRoomDetailView(DetailView):
    """DetailView that shows a single study room and its reviews."""
    model = StudyRoom
    template_name = "terrier_study/studyroom.html"
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object

        #retrieve all the reviews for this specfic study room
        context["reviews"] = UserReview.objects.filter(study_room=room).order_by("-published")

        # Check if the logged-in user has favorited this room
        if self.request.user.is_authenticated:
            # get the specific favorite object if it exists
            fav = UserFavorite.objects.filter(
                study_room=room,
                user=self.request.user
            ).first()
            context["user_favorite_obj"] = fav
            context["is_favorited"] = fav is not None
        else:
            context["user_favorite_obj"] = None
            context["is_favorited"] = False

        return context


class CreateReviewView(CheckLogin, CreateView):
    """Allows a logged-in user to create a review for a study room."""

    model = UserReview
    form_class = CreateReviewForm
    template_name = "terrier_study/create_review_form.html"

    def get_context_data(self, **kwargs):
        """inherit any context data and add room_id"""
        context = super().get_context_data(**kwargs)
        context["room_id"] = self.kwargs["room_id"] 
        return context

    def form_valid(self, form):
        """Called when a valid review form is submitted."""

        room = get_object_or_404(StudyRoom, pk=self.kwargs["room_id"])
        #instantiates a new review object
        form.instance.study_room = room
        #connects the review to the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the detail page of the reviewed study room."""
        room_id = self.kwargs["room_id"]
        return reverse("studyroom-detail", kwargs={"pk": room_id})

class UpdateReviewView(CheckLogin, UpdateView):
    """Allows a logged-in user to update their own review."""

    model = UserReview
    form_class = UpdateReviewForm
    template_name = "terrier_study/update_review_form.html"

    def get_queryset(self):
        """User may only edit their own reviews."""
        return UserReview.objects.filter(user=self.request.user)

    def get_success_url(self):
        """if the review is successfully updated, redirect to the study room detail page"""
        review = self.get_object()
        return reverse("studyroom-detail", kwargs={"pk": review.study_room.pk})
        
class DeleteReviewView(CheckLogin, DeleteView):
    """Allows a logged-in user to delete their own review."""

    model = UserReview
    template_name = "terrier_study/delete_review_confirm.html"
    context_object_name = "review"

    def get_queryset(self):
        """User may only delete their own reviews."""
        return UserReview.objects.filter(user=self.request.user) 

    def get_success_url(self):
        """if the review is successfully deleted, redirect to the study room detail page"""
        review = self.get_object()
        return reverse("studyroom-detail", kwargs={"pk": review.study_room.pk})
        
class AddFavoriteView(CheckLogin, TemplateView):
    """
    Allows a logged-in user to favorite a study room.
    """

    def dispatch(self, request, *args, **kwargs):

        # Check authentication
        if not request.user.is_authenticated:
            return redirect("login")


        # Retrieve the target study room
        room_id = self.kwargs["room_id"]
        room = get_object_or_404(StudyRoom, pk=room_id)

        # Create favorite relationship if it doesn’t already exist
        UserFavorite.objects.get_or_create(
            study_room=room,
            user=request.user
        )


        # Redirect back to the study room detail page
        return redirect("studyroom-detail", pk=room.pk)
    
class RemoveFavoriteView(CheckLogin, TemplateView):
    """
    Allows a logged-in user to remove a favorite study room.
    """

    def dispatch(self, request, *args, **kwargs):

        # Check authentication and redirect if not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        # Retrieve the favorite to be removed
        favorite_id = self.kwargs["pk"]
        favorite = get_object_or_404(UserFavorite, pk=favorite_id)

        # Save room before deletion
        room = favorite.study_room

        # Only delete if belongs to logged-in user
        if favorite.user == request.user:
            favorite.delete()

        # Redirect back to the room page (same as AddFavoriteView)
        return redirect("studyroom-detail", pk=room.pk)
    

class FavoriteListView(CheckLogin, ListView):
    """Show all favorites for the logged-in user."""

    model = UserFavorite
    template_name = "terrier_study/show_profile.html"
    context_object_name = "favorites"

    #get all the favorite objects for the logged-in user
    def get_queryset(self):
        return UserFavorite.objects.filter(
            user=self.request.user
        ).order_by("-date_saved")
    
class CreateProfileView(CreateView):
    """Create a new TerrierStudy profile for a user."""

    model = UserProfile
    form_class = CreateProfileForm
    template_name = "terrier_study/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """Add Django's UserCreationForm to context."""
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        """Handle creation of the Django User + TerrierStudy profile."""

        # Validate and create the Django User
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
        else:
            # Re-render with validation errors
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form)
            )

        # Log the new user in
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Attach the User to the TerrierStudy profile
        form.instance.user = user

        return super().form_valid(form)

    def get_success_url(self):
        """Go to the new user's profile page after registration"""
        return reverse("home")
    

class ProfileDetailView(CheckLogin, DetailView):
    """Show the profile of the logged-in user."""
    model = UserProfile
    template_name = "terrier_study/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        """Return the profile of the currently logged-in user."""
        user = self.request.user

        profile = UserProfile.objects.get(user=user)
        return profile

    def get_context_data(self, **kwargs):
        """Add any necessary context data such as favorites and reviews."""
        context = super().get_context_data(**kwargs)

        #get the logged-in user
        user = self.request.user

        #get all favorites and reviews for this user
        context["favorites"] = UserFavorite.objects.filter(user=user)
        context["reviews"] = UserReview.objects.filter(user=user)

        return context
    
class UpdateProfileView(CheckLogin, UpdateView):
    """Edit an already existing TerrierStudy profile."""

    model = UserProfile
    form_class = UpdateProfileForm
    template_name = "terrier_study/update_profile_form.html"

    def get_object(self):
        """Return the profile of the currently logged-in user."""
        return UserProfile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Add any necessary context data."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_object()
        return context

    def get_success_url(self):
        """Go to the user's profile page after updating."""
        return reverse("profile-detail")

    
def home(request):
    """Home page view with building filtering."""

    # Start with all study rooms
    rooms = StudyRoom.objects.all()

    # Apply the boolean filters
    for feature in ["on_campus", "id_required", "wifi", "outlets", "windows", "whiteboard"]:
        val = request.GET.get(feature)
        if val == "true":
            rooms = rooms.filter(**{feature: True})

    # Get buildings that have at least one of the filtered rooms
    buildings = Building.objects.filter(study_rooms__in=rooms).distinct()

    # Render the home template with buildings and Google Maps key
    return render(
        request,
        "terrier_study/home.html",
        {
            "google_key": settings.GOOGLE_MAPS_KEY,
            "buildings": buildings,
        }
    )

#----- API Views for JSON -----

class BuildingListAPIView(generics.ListAPIView):
    """Returns all buildings (for map pins)."""
    
    serializer_class = BuildingSerializer
    
    def get_queryset(self):
        """Optionally filter buildings by study room features."""
        qs = Building.objects.all()

        # Start with all study rooms
        rooms = StudyRoom.objects.all()

        # Apply the boolean filters
        for feature in ["on_campus", "id_required", "wifi", "outlets", "windows", "whiteboard"]:
            val = self.request.GET.get(feature)
            if val == "true":
                rooms = rooms.filter(**{feature: True})

        # Filter buildings to those that have at least one of the filtered rooms
        if rooms.exists():
            qs = qs.filter(study_rooms__in=rooms).distinct()

        return qs

class BuildingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''Retrieve, update, or delete a building.'''
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class StudyRoomListAPIView(generics.ListAPIView):
    """Returns all study rooms, with optional filtering by building or features."""
    serializer_class = StudyRoomSerializer

    def get_queryset(self):
        queryset = StudyRoom.objects.all()
        building_id = self.request.query_params.get('building', None)
        if building_id is not None:
            queryset = queryset.filter(building__id=building_id)
        
        # Feature filters
        features = {
            'on_campus': self.request.query_params.get('on_campus', None),
            'id_required': self.request.query_params.get('id_required', None),
            'wifi': self.request.query_params.get('wifi', None),
            'outlets': self.request.query_params.get('outlets', None),
            'windows': self.request.query_params.get('windows', None),
            'whiteboard': self.request.query_params.get('whiteboard', None),
        }
        for feature, value in features.items():
            if value is not None:
                if value.lower() == 'true':
                    queryset = queryset.filter(**{feature: True})
                elif value.lower() == 'false':
                    queryset = queryset.filter(**{feature: False})
        
        return queryset
    
class StudyRoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''DetailView of a specific studyroom.'''
    queryset = StudyRoom.objects.all()
    serializer_class = StudyRoomSerializer


class UserReviewListCreateAPIView(generics.ListCreateAPIView):
    '''List all reviews for a study room'''
    serializer_class = UserReviewSerializer

    def get_queryset(self):
        """Optionally filter reviews by study room ID."""
        queryset = UserReview.objects.all().order_by("-published")
        
        room_id = self.request.GET.get("room_id")
        if room_id:
            queryset = queryset.filter(study_room_id=room_id)

        return queryset
    
class UserReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''DetailView of a specific user review.'''
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer

class UserFavoriteListCreateAPIView(generics.ListCreateAPIView):
    '''List user favorites (by username) or create one.'''
    serializer_class = UserFavoriteSerializer

class UserFavoriteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''Detail view of a user favorite.'''
    queryset = UserFavorite.objects.all()
    serializer_class = UserFavoriteSerializer

class UserProfileListCreateAPIView(generics.ListCreateAPIView):
    '''Create a profile or list profiles (optional filter by user_name).'''
    serializer_class = UserProfileSerializer

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''Retrieve, update, or delete a user profile.'''
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer