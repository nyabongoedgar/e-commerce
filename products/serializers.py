from rest_framework import serializers
from .models import Category, ProductType, Product, ProductSpecification, ProductSpecificationValue, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = '__all__'

class ProductSpecificationValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecificationValue
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()  # Use a method to serialize inventory details

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'inventory']  # Include inventory in the fields

    def get_inventory(self, obj):
        # Return a dictionary with inventory details
        return {'quantity': obj.inventory.quantity}  # Adjust based on your Inventory model structure

