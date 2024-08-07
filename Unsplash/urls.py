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

from Unsplash import views

urlpatterns = [
    path('auth/callback', views.CallbackView.as_view()),
    path('random/multiple', views.MultipleView.as_view()),
    path('random', views.RandomView.as_view()),
    path('random/info', views.InfoView.as_view()),
    path('random/<str:size>', views.RandomView.as_view()),
    path('search/<str:color>', views.SearchView.as_view()),
    path('count', views.CountView.as_view()),
    path('', views.OAuthView.as_view()),
]
