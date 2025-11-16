from django.urls import path
from django.contrib import admin

from dadjokes.views import RandomJokePictureView, JokeListView, JokeDetailView, PictureListView, PictureDetailView

# Define URL patterns for the hw app
urlpatterns = [
    path("", RandomJokePictureView.as_view(), name="home"),
    path("random/", RandomJokePictureView.as_view(), name="random"),
    path("jokes/", JokeListView.as_view(), name="jokes"),
    path("joke/<int:pk>/", JokeDetailView.as_view(), name="joke"),
    path("pictures/", PictureListView.as_view(), name="pictures"),
    path("picture/<int:pk>/", PictureDetailView.as_view(), name="picture"),
]