from django.urls import path
from .views import create_shipping_address, process_payment

urlpatterns = [
    path('shipping-address/', create_shipping_address, name='create_shipping_address'),
    path('payment/<int:order_id>/', process_payment, name='process_payment'),
]
