#! /usr/bin/env python3
# coding: utf-8

'''This module inserts data from the openfoodfacts api into a database.
Run it using pipenv manage.py update_db.
'''

from django.core.management.base import BaseCommand
from datetime import date, datetime
import json
import os

import requests

from substituter.models import Product, Category


accepted_categories = ["boissons", "petits_dejeuners",
                       "produits_laitiers", "epicerie", "charcuteries"]

class Command(BaseCommand):
    help = 'Download data from the openfoodfacts api and write it into the database'

    def handle(self, *args, **options):
        '''Requests the open food facts api and unpacks the obtained data
        Each valid product (that is, with existing name, grade and categories)
        is added into the Products Table and linked to related Categories
        '''

        data = []

        results = {}
        results['products'] = []

        for category in accepted_categories:
            url = '''https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&json=1&tag_0=''' + category
            products = requests.get(url).json()["products"]

            for product in products:
                if "product_name" in product and "nutrition_grades" in product and "url" in product and "generic_name" in product and "image_url" in product and "code" in product:
                    categories = [category.strip().lower() for category
                                  in product["categories"].split(",")]
                    barcode = product['code']
                    name = product["product_name"]
                    grade = product["nutrition_grades"]
                    link = product["url"]
                    description = product["generic_name"]
                    image = product["image_url"]
                    fats = None
                    proteins = None
                    carbohydrates = None
                    sugars = None
                    salt = None
                    fibers = None

                    if product["nutriments"]:

                      if "fat_100g" in product["nutriments"]:
                          fats = product["nutriments"]["fat_100g"]
                      if "proteins_100g" in product["nutriments"]:
                          proteins = product["nutriments"]["proteins_100g"]
                      if "carbohydrates_100g" in product["nutriments"]:
                          carbohydrates = product["nutriments"]["carbohydrates_100g"]
                      if "sugars_100g" in product["nutriments"]:
                          sugars = product["nutriments"]["sugars_100g"]
                      if "salt_100g" in product["nutriments"]:
                          salt = product["nutriments"]["salt_100g"]
                      if "fibers_100g" in product["nutriments"]:
                          fibers = product["nutriments"]["fibers_100g"]

                    product, created = Product.objects.update_or_create(
                                                     barcode=barcode,
                                                     name=name,
                                                     grade=grade,
                                                     link=link, 
                                                     description=description, 
                                                     image=image, 
                                                     fats=fats, 
                                                     proteins=proteins, 
                                                     carbohydrates=carbohydrates, 
                                                     sugars=sugars, 
                                                     salt=salt, 
                                                     fibers=fibers
                                                    )
                    if created:
                        data.append("product #{} created".format(barcode))
                    else:
                        data.append("product #{} updated".format(barcode))


                    for category in categories:                    
                        cat, created = Category.objects.update_or_create(name=category)
                        product.categories.add(cat)
                        if created:
                            data.append("category {} created".format(category))

        with open('{}/update_log_{}.json'.format(os.environ.get('LOGS_PATH'),date.today()), 'w') as outfile:
            outfile.write(str(datetime.now()))
            for line in data:
                outfile.write('\n') 
                json.dump(line, outfile) 

