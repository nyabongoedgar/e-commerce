from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.models import Order, OrderItem
from.serializers import OrderSerializer
from products.models import Product
from cart.models import Cart
from rest_framework import generics
from.models import Order
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from.models import Order
from.serializers import OrderSerializer


class ListOrders(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        order = Order.objects.create(
            user=user,
            total_price=cart.calculate_total_price(),
            status="pending",
            payment_status="pending"
        )
        cart_items = cart.items.all()
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        cart.items.clear()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RetrieveOrder(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all()


# Additional views such as updating order status, processing payments, etc. can be added as needed.
