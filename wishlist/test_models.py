from django.test import TestCase
from .factories.factories import WishlistItemFactory
from .models import WishlistItem
from products.factories.factories import ProductFactory  # Adjust the import path as necessary
from accounts.factories.factories import CustomUserFactory  # Adjust the import path as necessary

class WishlistItemModelTests(TestCase):
    def test_wishlist_item_creation(self):
        wishlist_item = WishlistItemFactory()
        self.assertTrue(isinstance(wishlist_item, WishlistItem))
        self.assertEqual(str(wishlist_item), wishlist_item.product.name)

    def test_wishlist_item_unique_together(self):
        product = ProductFactory()
        user = CustomUserFactory(username='testuser', email='test@example.com', password='password')
        WishlistItem.objects.create(product=product, user=user)
        
        with self.assertRaises(Exception):
            WishlistItem.objects.create(product=product, user=user)
