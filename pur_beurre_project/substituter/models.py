'''
This file contains the models for the products and their categories.
'''


from django.db import models

class Category(models.Model):
    #Category model is simply a name
    name = models.CharField(max_length=50)

class Product(models.Model):
    '''
    The product model requires a name, nutrition grade, link to OFF,
    description and image to work. Six optional fields contain the nutritional
    informations about the product.
    Finally, each product is linked to at least one category.
    '''
    barcode = models.BigIntegerField(unique=True, null=True)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=1)
    link = models.URLField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.URLField(max_length=255)
    salt = models.FloatField(null=True)
    carbohydrates = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    fats = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    fibers = models.FloatField(null=True)
    categories = models.ManyToManyField(Category)