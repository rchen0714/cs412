from django.urls import path
from django.contrib import admin

from dadjokes.views import  RandomJokePictureView, JokeListView, JokeDetailView, PictureListView, PictureDetailView
from dadjokes.views import JokeListAPIView, JokeDetailAPIView, RandomJokeAPIView, PictureListAPIView, PictureDetailAPIView, RandomPictureAPIView

# Define URL patterns for the hw app
urlpatterns = [

    # ----- Regular Views for HTML -----
    path("", RandomJokePictureView.as_view(), name="home"),
    path("random/", RandomJokePictureView.as_view(), name="random"),

    path("jokes/", JokeListView.as_view(), name="jokes"),
    path("joke/<int:pk>/", JokeDetailView.as_view(), name="joke"),
    
    path("pictures/", PictureListView.as_view(), name="pictures"),
    path("picture/<int:pk>/", PictureDetailView.as_view(), name="picture"),

    # ----- API Views for JSON -----
    path('api/', RandomJokeAPIView.as_view()),
    path('api/random', RandomJokeAPIView.as_view()),

    path("api/jokes/", JokeListAPIView.as_view(), name="api_jokes"),
    path("api/joke/<int:pk>/", JokeDetailAPIView.as_view(), name="api_joke"),

    path("api/pictures/", PictureListAPIView.as_view(), name="api_pictures"),
    path("api/picture/<int:pk>/", PictureDetailAPIView.as_view(), name="api_picture"),
    path("api/pictures/random/", RandomPictureAPIView.as_view(), name="api_random_picture"),
]