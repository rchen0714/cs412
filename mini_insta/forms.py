# File: mini_insta/forms.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the forms for the mini_insta app.


from django import forms
from .models import Post, Profile

class CreatePostForm(forms.ModelForm):
    '''Define a form to create a new post''' 
    
    # This extra field allows for users to submit an image URL
    image_url = forms.URLField(required=False, label="Image URL")

    class Meta:
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    """Edit profile fields of a profile. all of the data attributes of the Profile class
        except NOT the user's username and join_date"""
    class Meta:
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']

class UpdatePostForm(forms.ModelForm):
    """Edit caption of a post."""
    class Meta:
        model = Post
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']
        


