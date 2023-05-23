from django.urls import path
from .views import OrderItemListCreateView, OrderItemAdmin

urlpatterns = [
    path('order_items/', OrderItemListCreateView.as_view(),
         name='order_item-list-create'),
    path('order_items_admin/', OrderItemAdmin.as_view(), name='order_items_admin'),
    # path('order_items/<int:pk>/', OrderItemRetrieveUpdateDeleteView.as_view(), name='orderitem-retrieve-update-delete'),
]
