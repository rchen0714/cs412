from django.urls import path
from . import views 
 
urlpatterns = [
    # map the URL (empty string) to the view
    path('', views.VoterListView.as_view(), name='home'),
    path('voters/', views.VoterListView.as_view(), name='voter_list'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', views.VoterGraphsView.as_view(), name='voter_graphs'),
]

