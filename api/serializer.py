from rest_framework import serializers
# from rest_framework.authtoken.admin import User
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =['id', 'name', 'new_price', 'category', 'description', 'weight', 'inventory']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email' ]

