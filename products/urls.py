from django.urls import path
from .views import (Products, UpdateProduct, AmenitiesView,
                    AddBookProductView, LastProductView, BookProducts, BookProductDetails)

urlpatterns = [

    path('last_products', LastProductView.as_view(), name='last_product'),
    path('book_product/<int:pk>',
         AddBookProductView.as_view(), name='book_product'),
    path('book_products/', BookProducts.as_view(), name='book_products'),
    path('book_products/<int:pk>', BookProductDetails.as_view(),
         name='book_product_details'),

    path('', Products.as_view(), name='add_product'),
    path('<int:pk>', UpdateProduct.as_view(), name='update_product'),

    # AmenitiesView
    path('amenities', AmenitiesView.as_view(), name='amenities'),
]
