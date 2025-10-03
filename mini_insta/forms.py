from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    '''Define a form to create a new post''' 
    
    image_url = forms.URLField(required=False, label="Image URL")

    class Meta:
        model = Post
        fields = ['caption']

        

