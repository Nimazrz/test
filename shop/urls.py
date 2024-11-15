from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:category_slug>/', views.index, name='index_by_slug')
]