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