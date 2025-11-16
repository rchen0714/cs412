"""
File: dadjokes/views.py
Author: Ruby Chen (rc071404@bu.edu)
Date: 11/16/2025
Description: Django views for the HTML and api views within 
the dadjokes application.
"""


from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.response import Response

import random
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
from .serializers import *

#----- Regular Views for HTML -----

class JokeListView(ListView):
    '''Display a list of all jokes'''
    
    model = Joke
    template_name = 'dadjokes/jokes.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    '''Display the instance of a single joke'''
    
    model = Joke
    template_name = 'dadjokes/joke_detail.html'
    context_object_name = 'joke'

class PictureListView(ListView):
    '''Display a list of all pictures'''
    
    model = Picture
    template_name = 'dadjokes/pictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    '''Display the instance of a single picture'''
    
    model = Picture
    template_name = 'dadjokes/picture_detail.html'
    context_object_name = 'picture'

class RandomJokePictureView(TemplateView):
    '''Display a random joke and picture'''

    template_name = 'dadjokes/random.html'
    context_object_name = 'random'

    def get_context_data(self, **kwargs):
        '''Get context data for the this random instance of a joke and picture'''

        context = super().get_context_data(**kwargs)
        context['joke'] = random.choice(Joke.objects.all())
        context['picture'] = random.choice(Picture.objects.all())
        
        return context
    

#----- API Views for JSON -----

class JokeListAPIView(generics.ListCreateAPIView):
    '''API view to retrieve list of jokes or create a new joke'''
    
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view to retrieve, update, or delete a joke'''
    
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class RandomJokeAPIView(generics.GenericAPIView):
    '''API view to get a random joke'''
    
    serializer_class = JokeSerializer 

    def get(self, request):
        '''Handle GET request for a random joke'''
        
        randomjoke = random.choice(Joke.objects.all())
        serializer = self.get_serializer(randomjoke)
        return Response(serializer.data)
    
class PictureListAPIView(generics.ListCreateAPIView):
    '''API view to retrieve list of pictures or create a new picture'''
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''API view to retrieve, update, or delete a picture'''
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.GenericAPIView):
    '''API view to get a random picture'''
    
    serializer_class = PictureSerializer 

    def get(self, request):
        '''Handle GET request for a random picture'''
        
        randompicture = random.choice(Picture.objects.all())
        serializer = self.get_serializer(randompicture)
        return Response(serializer.data)
    

    