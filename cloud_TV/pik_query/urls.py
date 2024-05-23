#!/usr/bin/env python3
from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.home_view, name='home'),
    path('home/search', views.submit, name='search'),
    path('result/', views.submit, name='result'),
    path('', RedirectView.as_view(url='/home')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
