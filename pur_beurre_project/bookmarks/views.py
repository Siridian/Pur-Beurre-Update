from django.shortcuts import render, get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required

from substituter.models import Product

@login_required
def bookmarked(request):
    #Displays all of a connected user's saved bookmarks
    context = {
    "bookmark_list": request.user.bookmarks.all()
    }
    return render(request, 'bookmarks/bookmarked.html', context)

@login_required
def save(request, substitute_id):
    '''
    Saves a product in a connected user's bookmark list using its pk,
    then displays the details about said product
    '''
    request.user.bookmarks.add(get_object_or_404(Product, id=substitute_id))
    context = {
    "product": Product.objects.get(pk=substitute_id)
    }
    return render(request, 'substituter/detail.html', context)
