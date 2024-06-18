from django.db import models

class Inventory(models.Model):
    # product = models.OneToOneField('products.Product', on_delete=models.CASCADE)
    # In your Inventory model
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='inventory_product')

    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.quantity}"

  
