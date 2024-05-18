#!/usr/bin/env python3
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('', RedirectView.as_view(url='/home')),
]
