
from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [

    # ----- API Views for JSON -----
    path("buildings/", BuildingListAPIView.as_view(), name="building-list"),
    path("buildings/<int:pk>/", BuildingDetailAPIView.as_view(), name="building"),
    path("studyrooms/", StudyRoomListAPIView.as_view(), name="studyroom-list"),
    path("studyrooms/<int:pk>/", StudyRoomDetailAPIView.as_view(), name="studyroom"),
    path("reviews/", UserReviewListCreateAPIView.as_view(), name="userreview-list"),
    path("reviews/<int:pk>/", UserReviewDetailAPIView.as_view(), name="userreview"),
    path("favorites/", UserFavoriteListCreateAPIView.as_view(), name="userfavorite-list"),
    path("favorites/<int:pk>/", UserFavoriteDetailAPIView.as_view(), name="userfavorite"),
    path("profiles/", UserProfileListCreateAPIView.as_view(), name="userprofile-list"),
    path("profiles/<int:pk>/", UserProfileDetailAPIView.as_view(), name="userprofile"),
]

