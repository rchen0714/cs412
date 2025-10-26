# File: mini_insta/forms.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines a custom mixin class for the
# mini_insta app. It uses the LoginRequiredMixin to ensure that
# certain views are only accessible to authenticated users.


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Profile

class CheckLogin(LoginRequiredMixin):
    '''A mixin to check if the user is logged in before accessing certain views.'''
    
    def get_login_url(self):
        '''Return the login URL for redirecting unauthenticated users.'''
        return reverse('login')

    def get_my_profile(self):
        '''Return the current Profile instance associated with the current user.'''
        return Profile.objects.get(user=self.request.user)