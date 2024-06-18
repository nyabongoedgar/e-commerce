# from .models import Category, ProductType, ProductSpecifications, Product, ProductSpecificationValue
# import random

# def create_sample_data():
#     # Creating categories
#     electronics_category = Category.objects.create(name="Electronics")
#     mobile_phones_category = Category.objects.create(name="Mobile Phones", parent=electronics_category)
#     smartphones_subcategory = Category.objects.create(name="Smartphones", parent=mobile_phones_category)
#     tablets_subcategory = Category.objects.create(name="Tablets", parent=electronics_category)
    
#     # Creating product types
#     smartphone_type = ProductType.objects.create(name="Smartphone")
#     tablet_type = ProductType.objects.create(name="Tablet")
    
#     # Creating product specifications
#     spec_screen_size = ProductSpecifications.objects.create(product_type=smartphone_type, name="Screen Size")
#     spec_battery_capacity = ProductSpecifications.objects.create(product_type=smartphone_type, name="Battery Capacity")
#     spec_weight = ProductSpecifications.objects.create(product_type=tablet_type, name="Weight")
    
#     # Creating a product
#     product = Product.objects.create(
#         category=smartphones_subcategory,
#         product_type=smartphone_type,
#         name="iPhone 13",
#         description="Latest iPhone model.",
#         price=999.99,
#         discount_price=None,
#         image="path/to/image.jpg"
#     )
    
#     # Creating product specification values
#     ProductSpecificationValue.objects.create(product=product, specification=spec_screen_size, value="6.1 inches")
#     ProductSpecificationValue.objects.create(product=product, specification=spec_battery_capacity, value="3247 mAh")
    
#     # Optionally, create a product with tablet type and its specifications
#     tablet_product = Product.objects.create(
#         category=tablets_subcategory,
#         product_type=tablet_type,
#         name="iPad Pro",
#         description="High-performance iPad.",
#         price=799.99,
#         discount_price=None,
#         image="path/to/ipad_image.jpg"
#     )
#     ProductSpecificationValue.objects.create(product=tablet_product, specification=spec_weight, value="1.5 kg")

# create_sample_data()



# seed.py

import random
from factory import Dict
from .factories.factories import CategoryFactory, ProductTypeFactory, ProductSpecificationFactory, ProductFactory, ProductSpecificationValueFactory, ProductVariantFactory, ProductSearchFactory, InventoryFactory

def create_sample_data():
    # Creating categories
    electronics_category = CategoryFactory(name="Electronics")
    mobile_phones_category = CategoryFactory(name="Mobile Phones", parent=electronics_category)
    smartphones_subcategory = CategoryFactory(name="Smartphones", parent=mobile_phones_category)
    tablets_subcategory = CategoryFactory(name="Tablets", parent=electronics_category)
    
    # Creating product types
    smartphone_type = ProductTypeFactory(name="Smartphone")
    tablet_type = ProductTypeFactory(name="Tablet")
    
    # Creating product specifications
    spec_screen_size = ProductSpecificationFactory(product_type=smartphone_type, name="Screen Size")
    spec_battery_capacity = ProductSpecificationFactory(product_type=smartphone_type, name="Battery Capacity")
    spec_weight = ProductSpecificationFactory(product_type=tablet_type, name="Weight")
    
    # Creating a product
    product = ProductFactory(
        category=smartphones_subcategory,
        product_type=smartphone_type,
        name="iPhone 13",
        description="Latest iPhone model.",
        price=999.99,
        image="path/to/image.jpg"
    )
    
    # Creating product specification values
    ProductSpecificationValueFactory(product=product, specification=spec_screen_size, value="6.1 inches")
    ProductSpecificationValueFactory(product=product, specification=spec_battery_capacity, value="3247 mAh")
    
    # Optionally, create a product with tablet type and its specifications
    tablet_product = ProductFactory(
        category=tablets_subcategory,
        product_type=tablet_type,
        name="iPad Pro",
        description="High-performance iPad.",
        price=799.99,
        image="path/to/ipad_image.jpg"
    )
    ProductSpecificationValueFactory(product=tablet_product, specification=spec_weight, value="1.5 kg")
    
    # Optionally, create inventories for products
    InventoryFactory(product=product, quantity=random.randint(0, 100))
    InventoryFactory(product=tablet_product, quantity=random.randint(0, 100))
    
    # Optionally, create product variants
    ProductVariantFactory(product=product, name="Variant 1", price=999.99, sku="IPHONE-VAR1", available=True)
    ProductVariantFactory(product=product, name="Variant 2", price=1099.99, sku="IPHONE-VAR2", available=True)

    # Optionally, create product search entries
    ProductSearchFactory(product=product, search_vector="iPhone 13 latest model")
    ProductSearchFactory(product=tablet_product, search_vector="iPad Pro high-performance")

create_sample_data()
