from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from cart.cart import Cart
from shop.models import Product


def add_to_cart(request, id):
    try:
        cart = Cart(request)
        if request.method == 'POST':
            product = get_object_or_404(Product, id=id)
            cart.add(product)
            context = {
                'item_count': len(cart),
                'total_price': cart.get_total_price()
            }
            return JsonResponse(context)
    except:
        return JsonResponse({"error" : 'invalid request'})



def detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})