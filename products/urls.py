from django.urls import path
from .views import (AddProduct)

urlpatterns = [
    path('', AddProduct.as_view(), name='add_product'),
]
