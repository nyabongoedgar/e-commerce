from django.test import TestCase
from django.db.models.expressions import F
# from.models import Product, ProductSearch
from .factories.factories import ProductFactory
from unittest.mock import patch, call

class ProductSearchTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup: Create sample products
        cls.product1 = ProductFactory(name="Example Product 1", description="Description 1")
        cls.product2 = ProductFactory(name="Example Product 2", description="Description 2")

    # @patch('django.contrib.postgres.search.SearchQuery')
    # @patch('django.contrib.postgres.search.SearchVector')
    # @patch('django.contrib.postgres.search.TrigramSimilarity')
    # @patch('django.contrib.postgres.search.SearchRank')
    # def test_product_search(self, MockSearchRank, MockTrigramSimilarity, MockSearchVector, MockSearchQuery):
        # Mock SearchQuery, SearchVector, TrigramSimilarity, and SearchRank
        # mock_query = "example"
        # MockSearchQuery.return_value = mock_query
        # MockSearchVector.return_value = mock_query
        # MockTrigramSimilarity.side_effect = [0.8, 0.7]  # Simulate different similarity scores
        # MockSearchRank.return_value = 0.85  # Simulate a rank score
        # print(f"{self.product1} results are here")
        # Execute the search method
        # results = ProductSearch.search(mock_query)
        # print(f"{results} results are here")
        # Assertions
        # self.assertEqual(len(results), 2)  # Expecting both products to match
        # self.assertEqual(results[0].product.name, "Example Product 1")
        # self.assertEqual(results[1].product.name, "Example Product 2")

        # Verify mocks were called with the correct parameters
        # MockSearchQuery.assert_called_once_with(mock_query)
        # MockSearchVector.assert_any_call('product__name', weight='A')
        # MockSearchVector.assert_any_call('product__description', weight='B')
        # MockTrigramSimilarity.assert_has_calls([
            # call('product__name', mock_query),
            # call('product__description', mock_query)
        # ], any_order=True)
        # MockSearchRank.assert_called_once_with(MockSearchVector(), MockSearchQuery())

