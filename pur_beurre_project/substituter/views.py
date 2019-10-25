'''
The views of the substituter app handles core features (such as index page)
as well as the research feature, and the detailed page of a given
food product.
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session

from sentry_sdk import capture_message

from .models import Product, Category

def index(request):
    #Displays home page
    return render(request, 'substituter/index.html')


def search(request):
    '''
    Searchs the database for the product with the most words in its title that
    match user's research. Then selects six other products with the most
    categories matching that of the base product, excluding those with worse
    food grades, and returns those six products as suggested substitutes.
    '''

    def _get_matching_product(input, criterion):
        '''
        This function reads each separate word in an input, and for each one 
        of them, creates a list of products with a given criterion matching
        said words. A given product can appear more than once.
        The function then returns a list of all the products found, sorted
        from most correlated to least correlated.
        '''

        results = []

        for word in input:
            if criterion == "name":
                matching_products = Product.objects.filter(name__icontains=word)
            elif criterion == "category":
                matching_products = Product.objects.filter(categories__name__icontains=word)
            for product in matching_products:
                results.append(product.pk)

        counted_results = []
        results.sort(reverse=True)
        x = 0
        while x < len (results):
            key = results[x]
            counted_results.append((key, results.count(key)))
            x += results.count(key)

        results_list = []

        for key in sorted(counted_results, 
                          key=lambda tuple: tuple[1], 
                          reverse = True):
            results_list.append(Product.objects.get(pk=key[0]))

        return results_list
        
    user_input = request.GET.get("query").split("+")

    try:
        base_product = _get_matching_product(user_input, "name")[0]

    except IndexError:
        context = {"status" : "error"}
        return render(request, 'substituter/search.html', context)

    category_list = [category.name 
                    for category 
                    in base_product.categories.all()]

    substitute_candidates = _get_matching_product(category_list, "category") 

    substitute_list = []

    for substitute in substitute_candidates:
        if substitute.grade < base_product.grade:
            substitute_list.append(substitute)

    if request.user.is_authenticated:
        context = {
        "status" : "ok connect",
        "base_product": base_product,
        "substitute_list": substitute_list[:6],
        "bookmarked_list": request.user.bookmarks.all()
        }

    else:
        context = {
        "status" : "ok",
        "base_product": base_product,
        "substitute_list": substitute_list[:6],
        "bookmarked_list": []
        }

    capture_message('New search : ' + request.GET.get("query"))

    return render(request, 'substituter/search.html', context)


def detail(request, product_id):
    #Displays detailed information about a given product using its pk
    product = get_object_or_404(Product, pk=product_id)
    context = {
    "product": product
    }
    return render(request, 'substituter/detail.html', context)


def legal(request):
    #Displays the legal mentions page
    return render(request, 'substituter/legal.html')
