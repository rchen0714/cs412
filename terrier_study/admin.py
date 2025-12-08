from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Building)
admin.site.register(StudyRoom)
admin.site.register(UserFavorite)
admin.site.register(UserReview)