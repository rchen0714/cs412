from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
import random

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


    