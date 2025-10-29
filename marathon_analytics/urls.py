from django.urls import path
from . import views 
 
urlpatterns = [
    # map the URL (empty string) to the view
	path('', views.ResultListView.as_view(), name='home'),
    path('results/', views.ResultListView.as_view(), name='results_list'),
    path('result/<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
]