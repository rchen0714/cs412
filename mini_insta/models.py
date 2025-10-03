# File: mini_insta/models.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the data models for the mini_insta app.

from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the model of a profile by an author'''
    
    
    username = models.TextField(blank=True) 
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this model instance'''
 
        return f"{self.username}: {self.display_name}'s Instagram Profile"
    
    def get_all_posts(self):
        '''Return all posts by this profile'''
        
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
    

class Post(models.Model):
    '''Encapsulate the model of a post by an author'''
    
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''

        return f"Post by {self.profile.username} on {self.timestamp}"
    
    def get_all_photos(self):
        '''Return all photos in this post'''
        
        photos = Photo.objects.filter(post=self)
        return photos
    
   
    

class Photo(models.Model):
    '''Encapsulate the model of a photo in a post'''
    
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''

        return f"Photo for {self.post} at {self.image_url} made on {self.timestramp}"
