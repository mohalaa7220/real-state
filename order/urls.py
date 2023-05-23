from django.urls import path
from .views import OrderItemListCreateView, OrderItemAdmin, OrderDetails, RemoveProductFromOrderView

urlpatterns = [
    path('order_items/', OrderItemListCreateView.as_view(),
         name='order_item-list-create'),
    path('order_items/<int:pk>', OrderDetails.as_view(), name='OrderDetails'),
    path('order_items/<int:order_id>/product/<int:product_id>/remove',
         RemoveProductFromOrderView.as_view(), name='remove-product-from-order'),
    path('order_items_admin/', OrderItemAdmin.as_view(), name='order_items_admin'),
]
