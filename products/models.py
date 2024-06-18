from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchVectorField
from django.db.models import Q
from django.core.cache import cache
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from inventory.models import Inventory


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.product_type} - {self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    field_tracker = models.JSONField(default=dict)
    inventory = models.ManyToManyField(Inventory, related_name='products') 

    def __str__(self):
        return self.name


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.specification.name}"
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=200)  # Name or label for the variant, e.g., "Large, Red"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_variants/', null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)  # SKU (Stock Keeping Unit) for the variant
    available = models.BooleanField(default=True)  # Indicates if the variant is available for purchase

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class ProductSearch(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),
        ]

    @classmethod
    def search(cls, query):
        if not query:
            return cls.objects.none()

        # Construct the search vector with weighted fields
        vector = SearchVector('product__name', weight='A') + SearchVector('product__description', weight='B')

        # Perform the search and rank the results
        queryset = cls.objects.annotate(
            rank=SearchRank(SearchQuery(query), vector)
        ).filter(rank__gte=0)

        return queryset


def filter_products(category_id=None, product_type_id=None, min_price=None, max_price=None):
    # Generate a cache key based on the function arguments
    cache_key = f'filtered_products_{category_id}_{product_type_id}_{min_price}_{max_price}'

    # Try to retrieve cached results
    cached_results = cache.get(cache_key)
    if cached_results:
        return cached_results

    # If not cached, perform the queryset operation
    query = Product.objects.all()

    if category_id:
        query = query.filter(category_id=category_id)

    if product_type_id:
        query = query.filter(product_type_id=product_type_id)

    if min_price is not None:
        query = query.filter(price__gte=min_price)

    if max_price is not None:
        query = query.filter(price__lte=max_price)

    # Cache the queryset results for future use
    results = list(query)
    cache.set(cache_key, results)

    return results
