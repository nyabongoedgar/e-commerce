from django.contrib import admin
from .models import Category, ProductType, Product, ProductSpecification, ProductSpecificationValue, ProductVariant

# List of models to register
models_to_register = [Category, ProductType, Product, ProductSpecification, ProductSpecificationValue, ProductVariant]

# Register all models in the list
for model in models_to_register:
    admin.site.register(model)
