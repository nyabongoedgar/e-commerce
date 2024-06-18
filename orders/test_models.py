from django.test import TestCase
from .models import Order, OrderItem
from .factories.factories import OrderFactory, OrderItemFactory
from products.factories.factories import ProductFactory
from accounts.factories.factories import CustomUserFactory

class OrderModelTest(TestCase):
    
    def setUp(self):
        self.user = CustomUserFactory()
        self.product1 = ProductFactory(price=100.00)
        self.product2 = ProductFactory(price=200.00)
        self.order = OrderFactory(user=self.user, total_price=300.00)

    def test_order_creation(self):
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_price, 300.00)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.payment_status, 'pending')

    def test_order_items(self):
        order_item1 = OrderItemFactory(order=self.order, product=self.product1, quantity=2)
        order_item2 = OrderItemFactory(order=self.order, product=self.product2, quantity=1)
        
        self.assertEqual(order_item1.subtotal, 200.00)
        self.assertEqual(order_item2.subtotal, 200.00)

        self.assertEqual(self.order.orderitem_set.count(), 2)

    def test_get_total_cost(self):
        OrderItemFactory(order=self.order, product=self.product1, quantity=2)
        OrderItemFactory(order=self.order, product=self.product2, quantity=1)
        
        self.assertEqual(self.order.get_total_cost(), 300.00)

class OrderItemModelTest(TestCase):

    def setUp(self):
        self.order = OrderFactory()
        self.product = ProductFactory(price=150.00)
        self.order_item = OrderItemFactory(order=self.order, product=self.product, quantity=3)

    def test_order_item_creation(self):
        self.assertIsInstance(self.order_item, OrderItem)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 3)

    def test_order_item_subtotal(self):
        self.assertEqual(self.order_item.subtotal, 450.00)
