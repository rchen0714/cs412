from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    hours_open = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} located at {self.address}"
    
class StudyRoom(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='study_rooms')
    name = models.CharField(max_length=100)
    floor = models.IntegerField()
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    on_campus = models.BooleanField(default=True)
    id_required = models.BooleanField(default=False)
    wifi = models.BooleanField(default=True)
    outlets = models.BooleanField(default=True)
    windows = models.BooleanField(default=False)
    whiteboard = models.BooleanField(default=False)

    def __str__(self):
        return f"Study room: {self.name} in {self.building.name} on floor {self.floor} room {self.room_number} (Capacity: {self.capacity})"


class UserFavorite(models.Model):
    study_room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='favorites')
    user_name = models.CharField(max_length=100)
    custom_roomname = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} favorited {self.study_room.name} at {self.date_saved} -- Notes: {self.notes}"
    
class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', null=True)
    study_room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='favorites')
    custom_roomname = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} favorited {self.study_room.name} at {self.date_saved} -- Notes: {self.notes}"
    
class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True)
    study_room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} ({self.rating} stars)"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="terrier_profile", null=True)

    bu_id = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    major = models.CharField(max_length=100)

    def __str__(self):
        return f"Profile: {self.user.username} ({self.major}, {self.year})"