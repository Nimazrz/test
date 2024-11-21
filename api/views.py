from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from api.serializer import *
from shop.models import Product

# Create your views here.


class ProductViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer