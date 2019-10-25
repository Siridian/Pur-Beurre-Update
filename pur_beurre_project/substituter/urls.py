'''
This file contains the urls of the substituter, which is the core app of this
project. It covers product research and details, and the legal mentions page.
'''

from django.conf.urls import url
from django.urls import path

from substituter import views

urlpatterns = [
    path(r'search/', views.search, name="search"),
    path(r'detail/<int:product_id>/', views.detail, name="detail"),
    path(r'legal/', views.legal, name="legal")
    ]