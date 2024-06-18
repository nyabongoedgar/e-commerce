import factory
from factory.django import DjangoModelFactory
from django.contrib.contenttypes.models import ContentType
from inventory.models import Inventory
from ..models import Category, ProductType, ProductSpecification, Product, ProductSpecificationValue, ProductVariant, ProductSearch

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    slug = factory.Faker('slug')
    parent = None

class ProductTypeFactory(DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Faker('word')

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = 'products.Product'

    name = factory.Faker('name')
    category = factory.SubFactory(CategoryFactory)
    product_type = factory.SubFactory(ProductTypeFactory)
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    
    # @factory.lazy_attribute
    # def discount_price(self):
    #     if factory.Faker('boolean', chance_of_getting_true=50).evaluate(None, None, {}):
    #         return factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True).evaluate(None, None, {})
    #     else:
    #         return None

    # image = factory.django.ImageField(color='blue')
    field_tracker = factory.Dict({})

    @factory.post_generation
    def inventory(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for inventory in extracted:
                self.inventory.add(inventory)

class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory

    product = factory.SubFactory(ProductFactory)  # Adjust based on your Product factory
    quantity = factory.Faker('pyint', min_value=0, max_value=100)

class ProductSpecificationFactory(DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = factory.Faker('word')
    content_type = factory.LazyFunction(lambda: ContentType.objects.get_for_model(Product))
    object_id = factory.SelfAttribute('content_object.id')
    content_object = factory.SubFactory(ProductFactory)

class ProductSpecificationValueFactory(DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = factory.Faker('word')

class ProductVariantFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    name = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    # image = factory.django.ImageField(color='green')
    sku = factory.Faker('ean13')
    available = factory.Faker('boolean')

class ProductSearchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSearch

    product = factory.SubFactory(ProductFactory)
    search_vector = factory.Faker('text')
