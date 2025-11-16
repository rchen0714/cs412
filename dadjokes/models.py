"""
File: dadjokes/models.py
Author: Ruby Chen (rc071404@bu.edu)
Date: 11/16/2025
Description: Django data models for the DadJokes application. Includes
the Joke model and the Picture model used by both the web views and api views.
"""



from django.db import models

# Create your models here.
class Joke(models.Model):
    '''A model representing a dad joke.'''
    text = models.TextField()
    contributor = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of the joke.'''
        return f"{self.joke} by {self.contributor} created at {self.timestamp}"
    
class Picture(models.Model):
    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image_url} by {self.contributor} created at {self.timestamp}"