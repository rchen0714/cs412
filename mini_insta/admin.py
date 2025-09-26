# File: mini_insta/admin.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: This file defines models the admin can alter for 
# the mini_insta app.

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)