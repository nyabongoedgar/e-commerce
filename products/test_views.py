from django.test import TestCase
import random
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIRequestFactory
from .views import (
    ProductViewSet, CategoryViewSet, ProductTypeViewSet,
    ProductSpecificationViewSet, ProductSpecificationValueViewSet
)

from .factories.factories import (
    CategoryFactory, ProductTypeFactory, ProductSpecificationFactory,
    ProductFactory, ProductSpecificationValueFactory
)

from .models import Product

class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductViewSet.as_view({'get': 'list', 'post': 'create'})
        self.detail_view = ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})
        self.search_view = ProductViewSet.as_view({'get': 'search'})

        self.product = ProductFactory()

    def test_list(self):
        request = self.factory.get('/api/products/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        request = self.factory.get(f'/api/products/{self.product.id}/')
        response = self.detail_view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = ProductFactory.build()  # Using build() to generate data without saving
        request = self.factory.post('/api/products/', data=data.__dict__)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        data = {
            'name': 'Updated Product',
            'price': '120.00',
        }
        request = self.factory.put(f'/api/products/{self.product.id}/', data=data)
        response = self.detail_view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Product')

    def test_delete(self):
        request = self.factory.delete(f'/api/products/{self.product.id}/')
        response = self.detail_view(request, pk=self.product.id)
        self.assertEqual(response.status_code, 204)

    def test_search(self):
        request = self.factory.get('/api/products/search/', {'query': 'Test'})
        response = self.search_view(request)
        self.assertEqual(response.status_code, 200)

"""
class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CategoryViewSet.as_view({'get': 'list', 'post': 'create'})
        self.detail_view = CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

        self.category = CategoryFactory()

    def test_list(self):
        request = self.factory.get('/api/categories/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        request = self.factory.get(f'/api/categories/{self.category.id}/')
        response = self.detail_view(request, pk=self.category.id)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = CategoryFactory.build()
        request = self.factory.post('/api/categories/', data=data.__dict__)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        data = {
            'name': 'Updated Category',
        }
        request = self.factory.put(f'/api/categories/{self.category.id}/', data=data)
        response = self.detail_view(request, pk=self.category.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Category')

    def test_delete(self):
        request = self.factory.delete(f'/api/categories/{self.category.id}/')
        response = self.detail_view(request, pk=self.category.id)
        self.assertEqual(response.status_code, 204)

class ProductTypeViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductTypeViewSet.as_view({'get': 'list', 'post': 'create'})
        self.detail_view = ProductTypeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

        self.product_type = ProductTypeFactory()

    def test_list(self):
        request = self.factory.get('/api/product-types/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        request = self.factory.get(f'/api/product-types/{self.product_type.id}/')
        response = self.detail_view(request, pk=self.product_type.id)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        data = ProductTypeFactory.build()
        request = self.factory.post('/api/product-types/', data=data.__dict__)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        data = {
            'name': 'Updated Product Type',
        }
        request = self.factory.put(f'/api/product-types/{self.product_type.id}/', data=data)
        response = self.detail_view(request, pk=self.product_type.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Product Type')

    def test_delete(self):
        request = self.factory.delete(f'/api/product-types/{self.product_type.id}/')
        response = self.detail_view(request, pk=self.product_type.id)
        self.assertEqual(response.status_code, 204)
"""
class ProductSpecificationViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductSpecificationViewSet.as_view({'get': 'list', 'post': 'create'})
        self.detail_view = ProductSpecificationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})
        self.product = ProductFactory()
        self.product_type = ProductTypeFactory()
        self.specification = ProductSpecificationFactory(product_type=self.product_type, content_object=self.product, content_type=ContentType.objects.get_for_model(Product), object_id=self.product.id)

    def test_list(self):
        request = self.factory.get('/api/product-specifications/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        request = self.factory.get(f'/api/product-specifications/{self.specification.id}/')
        response = self.detail_view(request, pk=self.specification.id)
        self.assertEqual(response.status_code, 200)

    # def test_create(self):
    #     data = ProductSpecificationFactory.build(id=299)
    #     print(f"{data.__dict__} - Dara")
    #     request = self.factory.post('/api/product-specifications/', data=data.__dict__)
    #     response = self.view(request)
    #     print(f"{response.data}")
    #     self.assertEqual(response.status_code, 201)

#     def test_update(self):
#         data = {
#             'name': 'Updated Specification',
#         }
#         request = self.factory.put(f'/api/product-specifications/{self.specification.id}/', data=data)
#         response = self.detail_view(request, pk=self.specification.id)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['name'], 'Updated Specification')

#     def test_delete(self):
#         request = self.factory.delete(f'/api/product-specifications/{self.specification.id}/')
#         response = self.detail_view(request, pk=self.specification.id)
#         self.assertEqual(response.status_code, 204)

# class ProductSpecificationValueViewSetTestCase(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.view = ProductSpecificationValueViewSet.as_view({'get': 'list', 'post': 'create'})
#         self.detail_view = ProductSpecificationValueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

#         self.product = ProductFactory()
#         self.specification = ProductSpecificationFactory(product_type=self.product.product_type)
#         self.specification_value = ProductSpecificationValueFactory(product=self.product, specification=self.specification)

#     def test_list(self):
#         request = self.factory.get('/api/product-specification-values/')
#         response = self.view(request)
#         self.assertEqual(response.status_code, 200)

#     def test_retrieve(self):
#         request = self.factory.get(f'/api/product-specification-values/{self.specification_value.id}/')
#         response = self.detail_view(request, pk=self.specification_value.id)
#         self.assertEqual(response.status_code, 200)

#     def test_create(self):
#         data = ProductSpecificationValueFactory.build()
#         request = self.factory.post('/api/product-specification-values/', data=data.__dict__)
#         response = self.view(request)
#         self.assertEqual(response.status_code, 201)

#     def test_update(self):
#         data = {
#             'value': 'Updated Value',
#         }
#         request = self.factory.put(f'/api/product-specification-values/{self.specification_value.id}/', data=data)
#         response = self.detail_view(request, pk=self.specification_value.id)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['value'], 'Updated Value')

#     def test_delete(self):
#         request = self.factory.delete(f'/api/product-specification-values/{self.specification_value.id}/')
#         response = self.detail_view(request, pk=self.specification_value.id)
#         self
