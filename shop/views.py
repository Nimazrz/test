from django.shortcuts import render, get_object_or_404, redirect
from .models import *


# Create your views here.

def index(request, category_slug=None):
    category = None
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)

    context ={
        'category':category,
        'products':products,
        'category_slug':category_slug,
        'categories':categories,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug, id):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'shop/detail.html', {'product':product})
