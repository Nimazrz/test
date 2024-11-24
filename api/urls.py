from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    path('products/', views.ProductViewSet.as_view(), name='api_products'),
    # path('users/', views.UserViewSet.as_view(), name='api_users'),

]