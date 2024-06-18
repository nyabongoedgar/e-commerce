import factory
from django.utils import timezone
from accounts.factories.factories import CustomUserFactory
from ..models import WishlistItem
from products.factories.factories import ProductFactory

class WishlistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishlistItem

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(CustomUserFactory)
    added_at = timezone.now()