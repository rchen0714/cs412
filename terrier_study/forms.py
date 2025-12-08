from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *

class CreateProfileForm(forms.ModelForm):
    """
    Form for creating a TerrierStudy user profile.
    Linked to the Django User via OneToOneField.
    """
    class Meta:
        model = UserProfile
        fields = ["bu_id", "year", "major"]

class UpdateProfileForm(forms.ModelForm):
    """
    Edit an existing TerrierStudy profile.
    """
    class Meta:
        model = UserProfile
        fields = ["bu_id", "year", "major"]

class CreateReviewForm(forms.ModelForm):
    """
    Create a new review for a study room.
    """
    class Meta:
        model = UserReview
        fields = ["rating", "text", "image_url"]


class UpdateReviewForm(forms.ModelForm):
    """
    Edit a previously written review.
    """
    class Meta:
        model = UserReview
        fields = ["rating", "text", "image_url"]

class CreateStudyRoomForm(forms.ModelForm):
    """
    Admin-like form allowing creation of study rooms.
    Useful if you want user-generated rooms.
    """
    class Meta:
        model = StudyRoom
        fields = [
            "building", "name", "floor", "room_number", "capacity",
            "description", "image_url",
            "on_campus", "id_required", "wifi",
            "outlets", "windows", "whiteboard",
        ]

class UpdateStudyRoomForm(forms.ModelForm):
    """
    Update an existing study room.
    """
    class Meta:
        model = StudyRoom
        fields = [
            "building", "name", "floor", "room_number", "capacity",
            "description", "image_url",
            "on_campus", "id_required", "wifi",
            "outlets", "windows", "whiteboard",
        ]