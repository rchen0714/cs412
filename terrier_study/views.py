from django.shortcuts import render
from importlib.resources import files
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login 

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .mixins import CheckLogin
from .forms import *

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

import random

from .models import * 
from .serializer import *


class BuildingListView(ListView):
    """Show all buildings."""
    model = Building
    template_name = "terrier_study/building_list.html"
    context_object_name = "buildings"

class BuildingDetailView(DetailView):
    """Show a single building and its study rooms."""
    model = Building
    template_name = "terrier_study/building_detail.html"
    context_object_name = "building"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        building = self.object
        context["rooms"] = StudyRoom.objects.filter(building=building)
        return context
    
class StudyRoomListView(ListView):
    """List all rooms with optional filtering."""
    model = StudyRoom
    template_name = "terrier_study/studyroom_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        queryset = StudyRoom.objects.all()

        building_id = self.request.GET.get("building")
        if building_id:
            queryset = queryset.filter(building_id=building_id)

        feature_filters = [
            "on_campus", "id_required", "wifi",
            "outlets", "windows", "whiteboard"
        ]

        for feature in feature_filters:
            val = self.request.GET.get(feature)
            if val == "true":
                queryset = queryset.filter(**{feature: True})
            elif val == "false":
                queryset = queryset.filter(**{feature: False})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["buildings"] = Building.objects.all()
        return context
    
class StudyRoomDetailView(DetailView):
    """Show one study room and its reviews."""
    model = StudyRoom
    template_name = "terrier_study/studyroom_detail.html"
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        context["reviews"] = UserReview.objects.filter(study_room=room).order_by("-published")
        return context
    
# class CreateReviewView(CheckLogin, CreateView):
#     """Create a review for a study room."""
#     model = UserReview
#     form_class = CreateReviewForm
#     template_name = "study/create_review_form.html"

#     def form_valid(self, form):
#         room_id = self.kwargs["room_id"]
#         room = get_object_or_404(StudyRoom, pk=room_id)

#         form.instance.study_room = room
#         form.instance.user_name = self.request.user.username

#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse(
#             "studyroom_detail",
#             kwargs={"pk": self.kwargs["room_id"]}
#         )

# class FavoriteListView(CheckLogin, ListView):
#     """Show all favorites for logged-in user."""
#     model = UserFavorite
#     template_name = "study/favorite_list.html"
#     context_object_name = "favorites"

#     def get_queryset(self):
#         username = self.request.user.username
#         return UserFavorite.objects.filter(user_name=username).order_by("-date_saved")
    
# class AddFavoriteView(CheckLogin, TemplateView):
#     """Add a room to the user's favorites."""
#     def dispatch(self, request, *args, **kwargs):
#         room_id = self.kwargs["room_id"]
#         room = get_object_or_404(StudyRoom, pk=room_id)

#         UserFavorite.objects.get_or_create(
#             user_name=request.user.username,
#             study_room=room
#         )

#         return redirect("studyroom_detail", pk=room_id)
    
# class RemoveFavoriteView(CheckLogin, TemplateView):
#     """Remove a room from favorites."""
#     def dispatch(self, request, *args, **kwargs):
#         pk = self.kwargs["pk"]
#         favorite = get_object_or_404(UserFavorite, pk=pk)

#         # Only delete if the favorite belongs to the current user
#         if favorite.user_name == request.user.username:
#             favorite.delete()

#         return redirect("favorite_list")
    
# class ProfileDetailView(CheckLogin, DetailView):
#     """Show the logged-in user's profile."""
#     model = UserProfile
#     template_name = "study/profile_detail.html"
#     context_object_name = "profile"

#     def get_object(self):
#         """Return only the logged-in user’s profile."""
#         return UserProfile.objects.get(user_name=self.request.user.username)
    
# class UpdateProfileView(CheckLogin, UpdateView):
#     """Edit user profile."""
#     model = UserProfile
#     form_class = UpdateProfileForm
#     template_name = "study/update_profile_form.html"

#     def get_object(self):
#         return UserProfile.objects.get(user_name=self.request.user.username)

#     def get_success_url(self):
#         return reverse("profile_detail")
    
# class ProfileDetailView(CheckLogin, DetailView):
#     model = UserProfile
#     template_name = "study/profile_detail.html"
#     context_object_name = "profile"

#     def get_object(self):
#         return UserProfile.objects.get(user_name=self.request.user.username)
    
# class UpdateProfileView(CheckLogin, UpdateView):
#     model = UserProfile
#     form_class = UpdateProfileForm
#     template_name = "study/update_profile_form.html"

#     def get_object(self):
#         return UserProfile.objects.get(user_name=self.request.user.username)

#     def get_success_url(self):
#         return reverse("profile_detail")
    
# class CreateProfileView(CheckLogin, CreateView):
#     model = UserProfile
#     form_class = CreateProfileForm
#     template_name = "study/create_profile_form.html"

#     def form_valid(self, form):
#         form.instance.user_name = self.request.user.username
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse("profile_detail")


# class CreateAccountView(CreateView):
#     """
#     Step 1: Create a Django User
#     Step 2: Create a linked UserProfile
#     """
#     template_name = "study/create_account_form.html"
#     form_class = CreateProfileForm   # profile form only

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["user_form"] = UserCreationForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         user_form = UserCreationForm(request.POST)
#         profile_form = CreateProfileForm(request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             # Create Django User
#             user = user_form.save()

#             # Log them in automatically
#             login(request, user)

#             # Create UserProfile linked to this User
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()

#             return redirect("profile_detail")

#         return render(request, self.template_name, {
#             "form": profile_form,
#             "user_form": user_form
#         })

#----- API Views for JSON -----

class BuildingListAPIView(generics.ListAPIView):
    """Returns all buildings (for map pins)."""
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

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
    '''Retrieve, update, or delete a study room.'''
    queryset = StudyRoom.objects.all()
    serializer_class = StudyRoomSerializer


class UserReviewListCreateAPIView(generics.ListCreateAPIView):
    '''List all reviews for a study room'''
    serializer_class = UserReviewSerializer

    def get_queryset(self):
        queryset = UserReview.objects.all().order_by("-published")
        
        room_id = self.request.GET.get("room_id")
        if room_id:
            queryset = queryset.filter(study_room_id=room_id)

        return queryset
    
class UserReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''Retrieve, update, or delete a user review.'''
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer

class UserFavoriteListCreateAPIView(generics.ListCreateAPIView):
    '''List user favorites (by username) or create one.'''
    serializer_class = UserFavoriteSerializer

    def get_queryset(self):
        username = self.request.GET.get("user_name")
        if not username:
            return UserFavorite.objects.none()
        return UserFavorite.objects.filter(user_name=username).order_by("-date_saved")

class UserFavoriteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''Retrieve, update, or delete a favorite.'''
    queryset = UserFavorite.objects.all()
    serializer_class = UserFavoriteSerializer

class UserProfileListCreateAPIView(generics.ListCreateAPIView):
    '''Create a profile or list profiles (optional filter by user_name).'''
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        username = self.request.GET.get("user_name")
        if username:
            return UserProfile.objects.filter(user_name=username)
        return UserProfile.objects.all()


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''Retrieve, update, or delete a user profile.'''
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer