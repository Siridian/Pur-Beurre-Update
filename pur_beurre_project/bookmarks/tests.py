'''
This module contains the various unit tests for the bookmarks app
'''

from django.test import TestCase
from django.test.client import Client

from substituter.models import Product
from accounts.models import User

class TestViewBookmarked(TestCase):
    #This class tests the Bookmarked view

    @classmethod 
    def setUpTestData(cls):
        #sets up a user with a bookmarked product

        p = Product.objects.create(name="testproduct")
        u = User.objects.create(email="testmail")
        u.set_password('testpass')
        u.save()
        u.bookmarks.add(p)
    
    def test_bookmarked_no_user_redirect(self):
        #tests that bookmarked view redirects anonymous users to login page

        response = self.client.get("/bookmarks/bookmarked", follow=True)

        self.assertRedirects(response, 
                            "/accounts/login/?next=/bookmarks/bookmarked/", 
                            status_code=301, 
                            target_status_code=200
        )

    def test_bookmarked_user_200(self):
        #tests that bookmarked view returns a 200 code for logged in users

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/bookmarks/bookmarked", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_bookmarked_gets_bookmarks(self):
        #tests that bookmarked view returns logged user's bookmarks in context

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/bookmarks/bookmarked", follow=True)

        self.assertEqual(response.context['bookmark_list'][0].name,
                         "testproduct"
        )


class TestViewSave(TestCase):
    #This class tests the Save view


    @classmethod
    def setUpTestData(cls):
        #sets up a product and a user

        p = Product.objects.create(id=1, name="testname")
        cls.u = User.objects.create(email="testmail")
        cls.u.set_password('testpass')
        cls.u.save()
    
    def test_save_no_user_redirect(self):
        #tests that save view redirects anonymous users to login page

        response = self.client.get("/bookmarks/save/1", follow=True)

        self.assertRedirects(response, 
                            "/accounts/login/?next=/bookmarks/save/1", 
                            status_code=302, 
                            target_status_code=200
        )

    def test_save_valid_id(self):
        '''
        tests that save view properly add an existing product to the
        request's user's bookmarks
        '''

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/bookmarks/save/1", follow=True)

        self.assertEqual(User.objects.get(id=self.u.id).bookmarks.all()[0].name, 
                         "testname"
        )

    def test_save_invalid_id(self):
        #tests that save view returns a 404 code for an non-existing product

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/bookmarks/save/2", follow=True)

        self.assertEqual(response.status_code, 404)