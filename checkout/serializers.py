from rest_framework import serializers
from .models import ShippingAddress, Payment

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zip_code']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['method', 'amount']
