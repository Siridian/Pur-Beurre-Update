'''
This module contains the various unit tests for the accounts app
'''

from django.test import TestCase
from django.test.client import Client

from .models import User, UserManager
from substituter.models import Product


# Utility

class TestAuthenticatedHTML(TestCase):
    #This class tests that the HTML generated differs for an authenticated user

    @classmethod 
    def setUpTestData(cls):
        #sets up a user

        u = User.objects.create(email="testmail")
        u.set_password('testpass')
        u.save()

    def test_HTML_authenticated_changes(self):
        #tests that bookmarked view returns a 200 code for logged in users

        c = Client()   
        
        response = c.get("/")
        self.assertContains(response, "Inscription")

        c.login(email='testmail', password='testpass')

        response = c.get("/")
        self.assertNotContains(response, "Inscription")


# Models

class TestUserModel(TestCase):
    #This class tests the user model

    def test_attributes(self):
        #tests that user's attributes are of the correct type when created

        user = User.objects.create(email='test@user.model',
                                   first_name="usermodelname",
                                   password="testpass"
        )
        p = Product.objects.create(name="productname")
        user.bookmarks.add(p)

        self.assertTrue(isinstance(user, User))
        self.assertEqual(type(user.email), str)
        self.assertEqual(type(user.first_name), str)
        self.assertEqual(type(user.password), str)
        self.assertTrue(isinstance(user.bookmarks.all()[0], Product))


# Views

class TestViewSignup(TestCase):
    #This class tests the Signup view

    def test_signup_works(self):
        #tests that a user is properly created through signup form

        response = self.client.post("/accounts/signup/", {
            'email': 'test@signup.works',
            'first_name': 'testworks',
            'password1': 'testpass',
            'password2': 'testpass'
            }
        )

        self.assertEqual(User.objects.get(email='test@signup.works').first_name,
                                          "testworks"
        )

    def test_signup_redirects(self):
        '''
        tests that a recently created user is redirected to index page
        and is logged in after signing up
        '''

        response = self.client.post("/accounts/signup/", {
            'email': 'test@signup.redirects',
            'first_name': 'testfn',
            'password1': 'testpass',
            'password2': 'testpass'
            }
        )

        self.assertRedirects(response, 
                             "/", 
                             status_code=302, 
                             target_status_code=200
        )
        self.assertIn('_auth_user_id', self.client.session)

    def test_signup_fails(self):
        #test that no user is created and the page reloaded if form is invalid

        response = self.client.post("/accounts/signup/", {
            'email': 'testmailsignupredirects',
            'first_name': 'testfn',
            'password1': 'testpass',
            'password2': 'testpass'
            }
        )

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)       
        

class TestViewDashboard(TestCase):
    #This Class tests the Dashboard view

    @classmethod 
    def setUpTestData(cls):
        #sets up a user

        u = User.objects.create(email="testmail")
        u.set_password('testpass')
        u.save()
    
    def test_dashboard_no_user_redirect(self):
        #tests that bookmarked view redirects anonymous users to login page

        response = self.client.get("/accounts/dashboard", follow=True)

        self.assertRedirects(response, 
                            "/accounts/login/?next=/accounts/dashboard/", 
                            status_code=301, 
                            target_status_code=200
        )

    def test_dashboard_user_200(self):
        #tests that bookmarked view returns a 200 code for logged in users

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/accounts/dashboard/", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_dashboard_gets_user(self):
        #tests that bookmarked view returns logged user's email in context

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/accounts/dashboard", follow=True)

        self.assertEqual(response.context['user'].email, "testmail")