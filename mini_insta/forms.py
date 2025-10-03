# File: mini_insta/forms.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the forms for the mini_insta app.


from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    '''Define a form to create a new post''' 
    
    # This extra field allows for users to submit an image URL
    image_url = forms.URLField(required=False, label="Image URL")

    class Meta:
        model = Post
        fields = ['caption']



