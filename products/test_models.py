from django.test import TestCase
from .models import filter_products
from .factories.factories import CategoryFactory, ProductTypeFactory, ProductSpecificationFactory, ProductFactory, ProductSpecificationValueFactory, ProductVariantFactory, ProductSearchFactory, InventoryFactory

class TestModels(TestCase):
    def test_category_creation(self):
        category = CategoryFactory()
        self.assertIsNotNone(category.name)
        self.assertIsNotNone(category.slug)
        self.assertEqual(str(category), category.name)

    def test_product_type_creation(self):
        product_type = ProductTypeFactory()
        self.assertIsNotNone(product_type.name)
        self.assertEqual(str(product_type), product_type.name)

    def test_product_specification_creation(self):
        product_specification = ProductSpecificationFactory()
        self.assertIsNotNone(product_specification.name)
        self.assertIsNotNone(product_specification.product_type)
        self.assertEqual(str(product_specification), f"{product_specification.product_type} - {product_specification.name}")

    def test_product_creation(self):
        product = ProductFactory()
        self.assertIsNotNone(product.name)
        self.assertIsNotNone(product.category)
        self.assertIsNotNone(product.product_type)
        self.assertEqual(str(product), product.name)

    def test_inventory_creation(self):
        inventory = InventoryFactory()
        self.assertGreaterEqual(inventory.quantity, 0)
        self.assertIsNotNone(inventory.product)
        self.assertEqual(str(inventory), f"{inventory.product.name}: {inventory.quantity}")

    def test_product_specification_value_creation(self):
        product_specification_value = ProductSpecificationValueFactory()
        self.assertIsNotNone(product_specification_value.value)
        self.assertIsNotNone(product_specification_value.product)
        self.assertIsNotNone(product_specification_value.specification)
        self.assertEqual(str(product_specification_value), f"{product_specification_value.product.name} - {product_specification_value.specification.name}")

    def test_product_variant_creation(self):
        product_variant = ProductVariantFactory(product=ProductFactory(name="unique ball"))
        self.assertIsNotNone(product_variant.name)
        self.assertGreater(product_variant.price, 0)
        self.assertIsNotNone(product_variant.product)
        self.assertEqual(str(product_variant), f"{product_variant.product.name} - {product_variant.name}")

    def test_product_search_creation(self):
        product_search = ProductSearchFactory()
        self.assertIsNotNone(product_search.product)

    def test_filter_products(self):
        category = CategoryFactory()
        product_type = ProductTypeFactory()
        product1 = ProductFactory(category=category, product_type=product_type, price=50)
        product2 = ProductFactory(category=category, product_type=product_type, price=150)
        
        results = filter_products(category_id=category.id, product_type_id=product_type.id, min_price=30, max_price=100)
        self.assertIn(product1, results)
        self.assertNotIn(product2, results)

    # def test_product_search(self):
    #     product = ProductFactory(name='Test Product', description='This is a test product')
    #     ProductSearch.objects.create(product=product)
        
    #     results = ProductSearch.search('Test')
    #     self.assertIn(product, [ps.product for ps in results])


# from.models import Product, ProductSearch

# class ProductSearchTestCase(TestCase):
#     def setUp(self):
#         # Create products for testing
#         self.product1 = ProductFactory(name="SpaceX Rocket", description="A rocket designed for space travel.")
#         self.product2 = ProductFactory(name="Apple iPhone", description="A smartphone by Apple.")

#         # Create a ProductSearch instance for each product
#         self.search1 = ProductSearch.objects.create(product=self.product1)
#         self.search2 = ProductSearch.objects.create(product=self.product2)

#     def test_search_returns_matching_products(self):
#         # Test searching for a term present in both products
#         query = "rocket"
#         results = ProductSearch.search(query)
#         self.assertIn(self.search1, results)
#         self.assertNotIn(self.search2, results)

#     def test_search_returns_no_results_for_nonexistent_term(self):
#         # Test searching for a term not present in any product
#         query = "nonexistent term"
#         results = ProductSearch.search(query)
#         self.assertEqual(len(results), 0)

#     def test_search_returns_ranked_results_based_on_relevance(self):
#         # Test searching for a term present in one product more prominently
#         query = "iPhone"
#         results = ProductSearch.search(query)
#         # Assuming the product with "iPhone" in its description is ranked higher
#         self.assertIn(self.search2, results)
#         self.assertNotIn(self.search1, results)

#     def tearDown(self):
#         # Optional cleanup after each test
#         pass
