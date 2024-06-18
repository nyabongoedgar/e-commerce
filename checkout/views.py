from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ShippingAddress, Payment
from .serializers import ShippingAddressSerializer, PaymentSerializer
from django.shortcuts import get_object_or_404
from orders.models import Order
from inventory.models import Inventory  # Adjust based on your actual model name

   

def update_inventory_on_checkout(product_id, quantity_to_reduce):
    inventory = Inventory.objects.get(product_id=product_id)
    inventory.quantity -= quantity_to_reduce
    inventory.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_shipping_address(request):
    serializer = ShippingAddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def process_payment(request, order_id):
    # Retrieve the order
    order = get_object_or_404(Order, id=order_id)

    # Initialize a flag to indicate if the order can be completed
    can_complete_order = False

    # Iterate over each item in the order
    for item in order.products.all():  # Assuming 'order_items' is a related name for OrderItem objects
        # Retrieve the inventory for the current item
        inventory_item = get_object_or_404(Inventory, product=item.product)

        # Check if the inventory has enough quantity for the order item
        if inventory_item.quantity >= item.quantity:
            inventory_item.quantity -= item.quantity
            inventory_item.save()
            can_complete_order = True
        else:
            # Not enough inventory for this item
            return Response({'error': f'Not enough inventory for {item.product.name}. Please try again.'}, status=400)

    # If we made it here, all items were successfully checked against inventory
    if can_complete_order:
        # Update the status of the order to 'completed'
        order.status = 'completed'
        order.save()

        # Optionally remove the order from the cart if it's still there
        if order.is_in_cart:
            order.delete()

        return Response({'message': 'Payment processed successfully'})

    else:
        # Payment failed due to insufficient inventory
        return Response({'error': 'Payment failed due to insufficient inventory. Please try again.'}, status=400)

