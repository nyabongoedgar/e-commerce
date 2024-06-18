from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    if not created:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    serializer = CartSerializer(cart)
    return Response(serializer.data)
