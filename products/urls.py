from django.urls import path
from .views import (Products, UpdateProduct, ProductsUser)

urlpatterns = [
    path('products_user', ProductsUser.as_view(), name='ProductsUser'),

    path('', Products.as_view(), name='add_product'),
    path('<int:pk>', UpdateProduct.as_view(), name='update_product'),
]
