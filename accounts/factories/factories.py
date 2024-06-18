import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = '+1234567890'
    shipping_address = factory.Faker('address')
    billing_address = factory.Faker('address')
    date_of_birth = factory.Faker('date_of_birth')
