from django.contrib.auth import get_user_model
from django.test import TestCase
from orders.models import Order, OrderItem
from products.models import Product, Category, ProductType, ProductSpecificationValue, ProductSpecification  
from wishlist.models import WishlistItem
from django.contrib.contenttypes.models import ContentType

class CustomUserTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )

        # Creating categories
        electronics_category = Category.objects.create(name="Electronics")

        # Creating product types
        tablet_type = ProductType.objects.create(name="Tablet")

        # Create a product
        self.product = Product.objects.create(
            category=electronics_category,
            product_type=tablet_type,
            name="iPhone 13",
            description="Latest iPhone model.",
            price=999.99,
            discount_price=None,
            image="path/to/image.jpg",
            field_tracker={},
        )

        # Get the content type for the Product model
        content_type = ContentType.objects.get_for_model(Product)

        spec_weight = ProductSpecification.objects.create(product_type=tablet_type, name="Weight", content_type=content_type, object_id=self.product.id)

        ProductSpecificationValue.objects.create(product=self.product, specification=spec_weight, value="1.5 kg")

       
        # Create an order associated with the user and order item
        order = Order.objects.create(user=self.user, total_price=0)
        # order.products.add(order_item)  

        # Create an order item associated with the product
        order_item = OrderItem.objects.create(order=order,product=self.product, quantity=10)

        # Update the total price of the order based on the order item's subtotal
        order.total_price = order_item.subtotal
        order.save()


    def test_custom_user_fields(self):
        """Test the fields of the CustomUser model."""
        user = get_user_model().objects.get(username=self.user.username)
        self.assertEqual(user.email, 'test@example.com')
        self.assertIsNone(user.phone_number)
        self.assertIsNone(user.shipping_address)
        self.assertIsNone(user.billing_address)
        self.assertIsNone(user.date_of_birth)
        self.assertEqual(user.orders.count(), 0)
        self.assertEqual(user.wishlist_items.count(), 0)

    def test_custom_user_relationships(self):
        """Test the relationships of the CustomUser model."""
        user = get_user_model().objects.get(username=self.user.username)
        # Test ManyToMany relationship with Order
        order = Order.objects.create(user=user, total_price=0)
        user.orders.add(order)
        self.assertIn(order, user.orders.all())
        
        """Test ManyToMany relationship with Product through WishlistItem"""
        item = WishlistItem.objects.create(product=self.product, user=self.user)
        user.wishlist_items.add(item)
        print(f'Printing wishlist: {user.wishlist_items.all()}')
        print(f'Printing item: {item.product}')
        self.assertTrue(user.wishlist_items.filter(product=self.product).exists())

    def test_str_method(self):
        """Test the __str__ method of the CustomUser model."""
        user = get_user_model().objects.get(username=self.user.username)
        self.assertEqual(str(user), self.user.username)
