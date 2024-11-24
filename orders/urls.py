from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    path('phone_verification/', views.phone_verification, name='phone_verification'),
    path('code_verification/', views.code_verification, name='code_verification'),
    path('create_order/', views.create_order, name='create_order'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
]