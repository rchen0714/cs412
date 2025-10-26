# File: mini_insta/models.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines the data models for the mini_insta app.

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the model of a profile by an author'''
    
    
    username = models.TextField(blank=True) 
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW

    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this model instance'''
 
        return f"{self.username}: {self.display_name}'s Instagram Profile"
    
    def get_all_posts(self):
        '''Return all posts by this profile'''
        
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
    
    
    def get_absolute_url(self):
        '''Return the url to access a particular profile instance.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    #Follower methods 
    def get_followers(self):
        '''Return all profiles that follow this profile'''
        
        #grab the Follow objects where the profile is being followed
        followers_query = Follow.objects.filter(profile=self)
        #return a list of the profiles within that object 
        followers = [follow.follower_profile for follow in followers_query]
        return followers
    
    def get_num_followers(self):
        '''Return the number of followers this profile has'''
        
        f_count = Follow.objects.filter(profile=self).count()
        return f_count 
    
    #Following methods 

    def get_following(self):
        '''Return all profiles that this profile is following'''
        #grab the Follow objects where the profile is the follower
        following_query = Follow.objects.filter(follower_profile=self)
        #return a list of the profiles within that object 
        following = [follow.profile for follow in following_query]
        return following
    
    def get_num_following(self):
        '''Return the number of profiles this profile is following'''
        f_count = Follow.objects.filter(follower_profile=self).count()
        return f_count
    
    def get_post_feed(self):
        '''Return all posts made by profiles this profile is following with a QuerySet'''
        
        following_profiles = Follow.objects.filter(follower_profile=self).values_list('profile', flat=True)
        feed = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        return feed
    
    #implementing helper method to help with the follow functionality
    def check_following(self, target_profile):
        '''Check if this profile is following the target_profile'''
        
        is_following = Follow.objects.filter(profile=target_profile, follower_profile=self).exists()
        return is_following


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
    
    def get_all_comments(self):
        '''Return all comments on this post'''
        
        comments = Comment.objects.filter(post=self).order_by('-timestamp')
        return comments
    
    def get_likes(self):
        '''Return all likes on this post'''
        
        likes = Like.objects.filter(post=self)
        return likes
    
    #implementing helper methods to help with the like functionality

    def check_liked_by(self, profile):
        '''Check if this post is liked by the given profile'''
        
        is_liked = Like.objects.filter(post=self, profile=profile).exists()
        return is_liked
   
class Photo(models.Model):
    '''Encapsulate the model of a photo in a post'''
    
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    image_url  = models.URLField(blank=True)        
    image_file = models.ImageField(blank=True)
    

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''

        #Will return a string based on whether the photo has an image URL or an image file
        
        if self.image_url:
            return f"Photo for {self.post} at {self.image_url} made on {self.timestamp}"
        elif self.image_file:
            return f"Photo for {self.post} at {self.image_file.url} made on {self.timestamp}"
        else:
            return f"{self.post} has no image, made on {self.timestamp}"
    

    def get_image_url(self):
        '''Return the image URL if it exists, otherwise return the image file path'''

        # returns the image URL if there is one, otherwise returns the image file path
        
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return None
        
#Now we will add three new models for assignment 6, Follow/Like/Comment 

class Follow(models.Model):
    '''Establishes a model of a follow relationship between two profiles'''
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the relationship between follower and followee'''

        follower_user = self.follower_profile.display_name or self.follower_profile.username
        followee_user = self.profile.display_name or self.profile.username
        return f"{follower_user} followed {followee_user} on {self.timestamp}"
    
class Comment(models.Model):
    '''Establishes a model of a comment made by a profile on a post'''
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the comment'''

        commenter = self.profile.display_name or self.profile.username
        return f"{commenter} - {self.timestamp}: {self.text}"
    
class Like(models.Model):
    '''Establishes a model of a like made by a profile on a post'''
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of the like'''

        liker = self.profile.display_name or self.profile.username
        likee = self.post.profile.display_name or self.post.profile.username
        return f"{liker} liked {likee}'s post on {self.timestamp}"

