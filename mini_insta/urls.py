
from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all'),
    path('show_all_profiles/', ProfileListView.as_view(), name='show_all'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
]