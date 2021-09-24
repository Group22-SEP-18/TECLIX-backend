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


class AssignVehicleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleProduct
        fields = '__all__'
