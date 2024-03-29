"""Unsplash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path

from Unsplash.views import auth_callback, random, oauth, random_empty, search, random_info, random_multiple

urlpatterns = [
    path('auth/callback', auth_callback),
    path('random/multiple', random_multiple),
    path('random', random_empty),
    path('random/info', random_info),
    path('random/<size>', random),
    path('search/<color>', search),
    path('', oauth),
]
