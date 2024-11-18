from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
    path('detail/', views.detail, name='cart_detail'),
    path('add_to_cart/<id>', views.add_to_cart, name='add_to_cart'),

]