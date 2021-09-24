from rest_framework import serializers
from .models import Product, Vehicle, VehicleProduct
from users.serializers import SalespersonDetailSerializer


# GET all products, Create a product POST
class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['created_by']


class SOProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['price']


# Single product GET, PUT, DELETE
class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Create a vehicle POST
class VehicleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ['created_by']


# Single Vehicle GET, PUT, DELETE
class VehicleViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleProductItemSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()

    class Meta:
        model = VehicleProduct
        fields = ['product', 'quantity']


# GET all vehicles and assigned product/salesperson details
class VehicleListViewSerializer(serializers.ModelSerializer):
    salesperson = SalespersonDetailSerializer()

    assigned_products = VehicleProductItemSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        extra_fields = ['assigned_products']
        model = Vehicle

# assign products and salesperson to a given vehicle
