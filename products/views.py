from rest_framework import viewsets, routers
from .mixins import InventoryMixin
from .models import Category, ProductType, Product, ProductSpecification, ProductSpecificationValue, ProductVariant
from .serializers import CategorySerializer, ProductSerializer, ProductSpecificationValue, ProductTypeSerializer, ProductSpecificationValueSerializer, ProductSpecificationSerializer, ProductVariantSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')

        if not query.strip():
            return Response([])

        search_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
        search_query = SearchQuery(query)
        rank = SearchRank(search_vector, search_query)

        results = Product.objects.annotate(rank=rank).filter(rank__gte=0.3).order_by('-rank')

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductSpecificationViewSet(viewsets.ModelViewSet):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer

class ProductSpecificationValueViewSet(viewsets.ModelViewSet):
    queryset = ProductSpecificationValue.objects.all()
    serializer_class = ProductSpecificationValueSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer


