# File: mini_insta/models.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the data models for the mini_insta app.

from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the model of a profile by an author'''
    
    # Defining fields for the Profile model
    
    username = models.TextField(blank=True) 
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this model instance'''
 
        return f"{self.username}: {self.display_name}'s Instagram Profile"
