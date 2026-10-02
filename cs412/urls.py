# File: urls.py
# Author: Ruby Chen (rc071404@bu.edu), 7/14/2004
# Description: URL configuration for cs412 project.

"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    # PythonAnywhere serves the domain root. TerrierStudy stays at
    # /terrier_study/ as well, which is the path used on cs-webapps.
    path('', RedirectView.as_view(pattern_name='terrier_study_home', permanent=False)),
    path('admin/', admin.site.urls),
    path('hw/', include('hw.urls')),
    path('quotes/', include('quotes.urls')),
    path('formdata/', include('formdata.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('blog/', include('blog.urls')),
    path('mini_insta/', include('mini_insta.urls')),
    path('marathon_analytics/', include('marathon_analytics.urls')), 
    path('voter_analytics/', include('voter_analytics.urls')), 
    path('dadjokes/', include('dadjokes.urls')),  
    path('terrier_study/', include('terrier_study.urls')), #NEW
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




