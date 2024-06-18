from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from.models import Product, ProductSearch

@receiver(post_save, sender=Product)
def update_product_search(sender, instance, **kwargs):
    # Get or create ProductSearch object for the Product instance
    # ProductSearch.objects.get_or_create(product=instance)

   # Note: Directly manipulating the SearchVectorField is not recommended.
    # If you need to update the search vector dynamically, consider doing so through Django's full-text search API or model methods.
    pass