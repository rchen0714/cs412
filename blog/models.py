# blog/model.py 
# define data models for the blog application 

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
 

# Create your models here.

class Article(models.Model):
    '''Encalsulate the model of a blog Article by an author'''
    
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW
    
    # image_url = models.URLField(blank=True)

    image_file = models.ImageField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this model instance'''

        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        '''Return the url to access a particular article instance.'''
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        '''Return all comments related to this article instance'''
        comments = Comment.objects.filter(article=self)
        return comments

class Comment(models.Model):
    '''Encapsulate the model of a comment on a blog article'''

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''

        return f'{self.text}'
    
    