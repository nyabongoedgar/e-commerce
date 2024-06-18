import factory
from factory.django import DjangoModelFactory
from ..models import Cart, CartItem
from products.factories.factories import ProductFactory
from accounts.factories.factories import CustomUserFactory

class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(CustomUserFactory)

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                CartItemFactory(cart=self, product=product)

class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Sequence(lambda n: n + 1)
