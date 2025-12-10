
# File: terrier_study/urls.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: These are the URL configuration for the terrier_study application.

from django.urls import path
from django.contrib import admin
from .views import *
from django.contrib.auth import views as auth_views  

urlpatterns = [

    path("", home, name="home"),
    
    path("buildings/", BuildingListView.as_view(), name="building-list"),
    path("buildings/<int:pk>/", BuildingDetailView.as_view(), name="building-detail"),
    path("buildings/map/", TemplateView.as_view(template_name="terrier_study/building_maps.html"), name="building-map"),

    path("studyrooms/create/", CreateStudyRoomView.as_view(), name="create-studyroom"),
    path("studyrooms/", StudyRoomListView.as_view(), name="studyroom-list"),
    path("studyrooms/<int:pk>/", StudyRoomDetailView.as_view(), name="studyroom-detail"),

    path("studyrooms/<int:room_id>/review/add/", CreateReviewView.as_view(), name="create-review"),
    path("reviews/<int:pk>/update/", UpdateReviewView.as_view(), name="update-review"),
    path("reviews/<int:pk>/delete/", DeleteReviewView.as_view(), name="delete-review"),

    path("favorites/", FavoriteListView.as_view(), name="favorite-list"),
    path("favorites/add/<int:room_id>/", AddFavoriteView.as_view(), name="add-favorite"),
    path("favorites/remove/<int:pk>/", RemoveFavoriteView.as_view(), name="remove-favorite"),

    path("profile/create/", CreateProfileView.as_view(), name="create-profile"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/update/", UpdateProfileView.as_view(), name="update-profile"),

    path("login/", auth_views.LoginView.as_view(template_name="terrier_study/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="terrier_study/logged_out.html"), name="logout"),
    path("register/", CreateProfileView.as_view(), name="register"),


    # ----- API Views for JSON -----
    path("api/buildings/", BuildingListAPIView.as_view(), name="api-building-list"),
    path("api/buildings/<int:pk>/", BuildingDetailAPIView.as_view(), name="api-building"),
    path("api/studyrooms/", StudyRoomListAPIView.as_view(), name="api-studyroom-list"),
    path("api/studyrooms/<int:pk>/", StudyRoomDetailAPIView.as_view(), name="api-studyroom"),
    path("api/reviews/", UserReviewListCreateAPIView.as_view(), name="api-review-list"),
    path("api/reviews/<int:pk>/", UserReviewDetailAPIView.as_view(), name="api-review-detail"),
    path("api/favorites/", UserFavoriteListCreateAPIView.as_view(), name="api-favorite-list"),
    path("api/favorites/<int:pk>/", UserFavoriteDetailAPIView.as_view(), name="api-favorite-detail"),
    path("api/profiles/<int:pk>/", UserProfileDetailAPIView.as_view(), name="api-profile-detail"),
]

