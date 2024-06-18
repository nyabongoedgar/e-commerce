import factory
from factory.django import DjangoModelFactory
from products.factories.factories import ProductFactory
from ..models import Order, OrderItem
from accounts.factories.factories import CustomUserFactory

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(CustomUserFactory)
    total_price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    status = 'pending'
    payment_status = 'pending'
    is_in_cart = False
    address = factory.Faker('address')
    postal_code = factory.Faker('postcode')
    city = factory.Faker('city')
    country = factory.Faker('country')

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=10)
