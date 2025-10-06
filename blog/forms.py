
from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'text', 'image_file']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']
        