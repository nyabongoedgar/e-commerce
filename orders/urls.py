from django.urls import path
from.views import ListOrders, CreateOrder, RetrieveOrder

urlpatterns = [
    path('orders/', ListOrders.as_view(), name='list-orders'),
    path('orders/create/', CreateOrder.as_view(), name='create-order'),
    path('orders/<int:order_id>/', RetrieveOrder.as_view(), name='retrieve-order'),
]
