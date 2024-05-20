#!/usr/bin/env python3
from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('home/search', views.submit, name='search'),
    path('result/', views.submit, name='result'),
    path('', RedirectView.as_view(url='/home')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
