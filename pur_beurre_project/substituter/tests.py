'''
This module contains the various unit tests for the substituter app
'''

from django.test import TestCase
from django.test.client import Client
from django.http import JsonResponse
import json

from .models import Product, Category
from accounts.models import User


# Models

class TestModels(TestCase):
    #This class tests the product and category models

    def test_product(self):
        #tests that product's attributes are of the correct type when created

        product = Product.objects.create(
        name = "testname",
        grade = "a",
        link = "test.com",
        description = "testdescr",
        image = "test.image",
        salt = 13.2,
        carbohydrates = 8.0,
        sugars = 5.7,
        fats = 6.6,
        proteins = 55.1,
        fibers = 3.0,
        )
        cat = Category.objects.create(name="test")

        product.categories.add(cat)

        self.assertTrue(isinstance(product, Product))
        self.assertEqual(type(product.name), str)
        self.assertEqual(type(product.grade), str)
        self.assertEqual(type(product.link), str)
        self.assertEqual(type(product.description), str)
        self.assertEqual(type(product.image), str)
        self.assertEqual(type(product.salt), float)
        self.assertEqual(type(product.carbohydrates), float)
        self.assertEqual(type(product.sugars), float)
        self.assertEqual(type(product.fats), float)
        self.assertEqual(type(product.proteins), float)
        self.assertEqual(type(product.fibers), float)
        self.assertTrue(isinstance(product.categories.all()[0], Category))

    def test_category(self):
        #tests that category's name is of the correct type when created

        cat = Category.objects.create(name="test")
        self.assertTrue(isinstance(cat, Category))
        self.assertEqual(type(cat.name), str)


# Views

class TestViewIndex(TestCase):
    #This class tests the Index view

    def test_index_200(self):
        #tests that index view returns a 200 code

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)


class TestViewSearch(TestCase):
    #This class tests the Search view

    @classmethod 
    def setUpTestData(cls):
        #sets up various products and categories, as well as a user

        cata = Category.objects.create(name="cata")
        catb = Category.objects.create(name="catb")
        catc = Category.objects.create(name="catc")
        catd = Category.objects.create(name="catd")

        producta = Product.objects.create(name="alpha beta")
        productb = Product.objects.create(name="beta gamma", grade = 'c')
        productc = Product.objects.create(name="gamma delta")
        productd = Product.objects.create(name="substitute", grade = 'b')
        producte = Product.objects.create(name="best substitute", grade='b')
        productf = Product.objects.create(name="no substitute", grade='b')
        productg = Product.objects.create(name="unealthy substitute", grade='d')

        productb.categories.add(cata, catb, catc)
        productd.categories.add(cata)
        producte.categories.add(cata, catb)
        productf.categories.add(catd)
        productg.categories.add(cata, catb, catc)

        u = User.objects.create(email="testmail")
        u.set_password('testpass')
        u.save()
        u.bookmarks.add(producte)

    def test_search_200(self):
        #tests that search view returnes 200 code with proper query

        response = self.client.get("/substituter/search/", 
                                   {'query': 'gamma+beta'}, 
                                   follow=True
        )

        self.assertEqual(response.status_code, 200)

    def test_search_find_base_product(self):
        #tests that search view finds most relevant product based on query

        response = self.client.get("/substituter/search/",
                                   {'query': 'gamma+beta'}
        )

        self.assertEqual(response.context['base_product'].name, "beta gamma")

    def test_search_find_no_base_product(self):
        #tests that search view returns error code when no product matches query

        response = self.client.get("/substituter/search/",
                                   {'query': 'epsilon'}
        )

        self.assertEqual(response.context['status'], "error")

    def test_search_correct_substitute_order(self):
        """
        tests that the subtitutes proposed for a given product are of better
        grade, and sorted according to category relevance
        """

        response = self.client.get("/substituter/search/",
                                   {'query': 'gamma+beta'}
        )

        self.assertEqual(len(response.context['substitute_list']), 2)
        self.assertEqual(response.context['substitute_list'][0].name,
                         "best substitute"
        )

    def test_search_gets_boomkarks(self):
        #tests that search view returns request's user's bookmarks

        c = Client()     
        c.login(email='testmail', password='testpass')

        response = c.get("/substituter/search/", {'query': 'gamma+beta'})

        self.assertEqual(response.context['bookmarked_list'][0].name,
                         "best substitute"
        )


class TestViewDetail(TestCase):
    #This class tests the Detail view

    @classmethod 
    def setUpTestData(cls):
        #sets up a single product, with id 1 (for easier querying)

        Product.objects.create(id = 1, name = "testname")

    def test_detail_valid_id(self):
        #tests that detail view returns a 200 code for an existing product

        response = self.client.get("/substituter/detail/1", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_detail_invalid_id(self):
        #tests that detail view returns a 404 code for an non-existing product

        response = self.client.get("/substituter/detail/2", follow=True)

        self.assertEqual(response.status_code, 404)

    def test_detail_correct_context(self):
        #tests that detail view sends product's informations through context

        response = self.client.get("/substituter/detail/1", follow=True)

        self.assertEqual(response.context['product'].name, "testname")


class TestViewAutocomplete(TestCase):
    #This class tests the Autocomplete view

    @classmethod 
    def setUpTestData(cls):
        #sets up several products with different names

        Product.objects.create(name = "foo")
        Product.objects.create(name = "bar")
        Product.objects.create(name = "foobar")
        Product.objects.create(name = "foba")

    def test_autocomplete_json_type(self):
        #tests that detail view returns a 200 code for an existing product

        response = self.client.get("/substituter/autocomplete", 
                                   {'term': 'foobar'},
                                   follow=True
        )
        self.assertEqual(type(response), JsonResponse)


    def test_autocomplete_suggestions(self):
        #tests that detail view returns a 200 code for an existing product

        response = self.client.get("/substituter/autocomplete", 
                                   {'term': 'fo'},
                                   follow=True
        )
        self.assertEqual(json.loads(response.content), ['foo', 'foobar', 'foba'])

        response = self.client.get("/substituter/autocomplete", 
                                   {'term': 'bar'},
                                   follow=True
        )
        self.assertEqual(json.loads(response.content), ['bar', 'foobar'])

        response = self.client.get("/substituter/autocomplete", 
                                   {'term': 'foo'},
                                   follow=True
        )
        self.assertEqual(json.loads(response.content), ['foo', 'foobar'])

        response = self.client.get("/substituter/autocomplete", 
                                   {'term': 'foba'},
                                   follow=True
        )
        self.assertEqual(json.loads(response.content), ['foba'])

        response = self.client.get("/substituter/autocomplete", 
                                   {'term': 'barfoo'},
                                   follow=True
        )
        self.assertEqual(json.loads(response.content), [])


class TestViewLegal(TestCase):
    #This class tests the Legal view

    def test_legal_200(self):
        #tests that legal view returns a 200 code

        response = self.client.get("/substituter/legal/")

        self.assertEqual(response.status_code, 200)