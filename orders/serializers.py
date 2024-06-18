from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_price', 'status', 'created_at', 'updated_at',
            'payment_status', 'is_in_cart', 'address', 'postal_code', 'city', 'country', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('orderitem_set', None)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.status = validated_data.get('status', instance.status)
        instance.payment_status = validated_data.get('payment_status', instance.payment_status)
        instance.is_in_cart = validated_data.get('is_in_cart', instance.is_in_cart)
        instance.address = validated_data.get('address', instance.address)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.save()

        if items_data:
            for item_data in items_data:
                item_id = item_data.get('id')
                if item_id:
                    item = OrderItem.objects.get(id=item_id, order=instance)
                    item.product = item_data.get('product', item.product)
                    item.quantity = item_data.get('quantity', item.quantity)
                    item.save()
                else:
                    OrderItem.objects.create(order=instance, **item_data)

        return instance
