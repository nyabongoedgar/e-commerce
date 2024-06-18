# wish/models.py
from django.db import models
from django.conf import settings
from products.models import Product

class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user',)

    def __str__(self) -> str:
        return self.product.name
