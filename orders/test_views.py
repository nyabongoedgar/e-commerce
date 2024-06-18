from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Order, OrderItem
from .serializers import OrderSerializer
from .factories.factories import OrderFactory, OrderItemFactory
from products.factories.factories import ProductFactory
from accounts.factories.factories import CustomUserFactory
from cart.factories.factories import CartFactory, CartItemFactory

class OrderViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUserFactory()
        self.product1 = ProductFactory(price=100.00)
        self.product2 = ProductFactory(price=200.00)
        self.cart = CartFactory(user=self.user)
        self.cart_item1 = CartItemFactory(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItemFactory(cart=self.cart, product=self.product2, quantity=1)
        self.order = OrderFactory(user=self.user)
        self.order_item1 = OrderItemFactory(order=self.order, product=self.product1, quantity=2)
        self.order_item2 = OrderItemFactory(order=self.order, product=self.product2, quantity=1)
        self.client.force_authenticate(user=self.user)

    def test_list_orders(self):
        response = self.client.get(reverse('list-orders'))
        orders = Order.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)
        print(f"{response.data}: Response.data")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    
    def test_create_order(self):
        response = self.client.post(reverse('create-order'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.filter(user=self.user).count(), 2)
        self.assertEqual(OrderItem.objects.count(), 4)
        order = Order.objects.get(id=response.data['id'])
        self.assertEqual(order.total_price, self.cart.calculate_total_price())
        self.assertEqual(order.orderitem_set.count(), 2)

    # def test_retrieve_order(self):
    #     response = self.client.get(reverse('retrieve-order', args=[self.order.id]))
    #     order = Order.objects.get(id=self.order.id)
    #     serializer = OrderSerializer(order)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, serializer.data)
