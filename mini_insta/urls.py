
from django.urls import path
from .views import ShowAllView, ProfileView

urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all'),
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
]