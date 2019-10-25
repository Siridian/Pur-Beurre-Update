'''
This file contains the urls used in the accounts app.
It allows the users to signup and manage their accounts.
'''

from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path

from accounts import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard')
]