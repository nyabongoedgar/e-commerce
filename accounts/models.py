from django.contrib.auth.models import AbstractUser
from django.db import models
from orders.models import Order
from wishlist.models import WishlistItem

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    orders = models.ManyToManyField(Order, related_name='my_orders', blank=True)
    # Wishlist
    wishlist_items = models.ManyToManyField(WishlistItem, related_name='users')
    def __str__(self):
        return self.username
