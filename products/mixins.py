from rest_framework import mixins, viewsets
from.models import Product, Inventory  # Import your Product and Inventory models

class InventoryMixin(mixins.CreateModelMixin, mixins.UpdateModelMixin):
    def add_stock(self, product_id, quantity):
        inventory = Inventory.objects.get(product_id=product_id)
        inventory.quantity += quantity
        inventory.save()

    def reduce_stock(self, product_id, quantity):
        inventory = Inventory.objects.get(product_id=product_id)
        inventory.quantity -= quantity
        inventory.save()

    def adjust_quantity(self, product_id, quantity):
        inventory = Inventory.objects.get(product_id=product_id)
        inventory.quantity += quantity  # Increase quantity if positive, decrease if negative
        inventory.save()

    def perform_create(self, serializer):
        # Implement inventory logic when creating a new product
        product = serializer.save()  # Save the product instance
        # Assuming you have a method to update inventory; adjust as necessary
        self.add_stock(product.id, product.quantity)  # Call your inventory update method

    def perform_update(self, serializer):
        # Implement inventory logic when updating a product
        product = serializer.save()  # Save the updated product instance
        # Assuming you have a method to update inventory; adjust as necessary
        self.adjust_quantity(product.id, product.quantity)   # Call your inventory update method

    def update_inventory(self, product_id, quantity):
        # Placeholder for your inventory update logic
        # This method should decrease the inventory count for the given product_id
        # and increase it if the quantity is negative (indicating a return or adjustment)
        inventory = Inventory.objects.get(product_id=product_id)
        inventory.quantity -= quantity
        inventory.save()

    

