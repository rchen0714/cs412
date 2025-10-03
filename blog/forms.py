
from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'text', 'image_url']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        