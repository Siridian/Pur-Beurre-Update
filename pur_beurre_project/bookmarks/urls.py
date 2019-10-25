'''
This file contains the urls used in the bookmarks app.
Their aim is to save specific products in the bookmark list, and
display that list to the user.
They can only be used by a connected user.
'''


from django.conf.urls import url
from django.urls import path

from bookmarks import views

urlpatterns = [
    path(r'save/<int:substitute_id>', views.save, name="save"),
    path(r'bookmarked/', views.bookmarked, name="bookmarked")
]