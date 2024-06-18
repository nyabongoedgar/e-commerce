from django.contrib.auth import get_user_model
from django.db import models
from products.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def calculate_total_price(self):
        """
        Calculate the total price of all items in the cart.
        Assumes that each Product has a price attribute.
        """
        total_price = 0
        for cart_item in self.items.all():
            total_price += cart_item.product.price * cart_item.quantity
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
