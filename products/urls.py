from rest_framework import routers
from .views import  CategoryViewSet, ProductTypeViewSet, ProductViewSet, ProductSpecificationViewSet, ProductSpecificationValueViewSet, ProductVariantViewSet
# Define router and register viewsets
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-specifications', ProductSpecificationViewSet)
router.register(r'product-specification-values', ProductSpecificationValueViewSet)
router.register(r'product-variants', ProductVariantViewSet)

urlpatterns = router.urls