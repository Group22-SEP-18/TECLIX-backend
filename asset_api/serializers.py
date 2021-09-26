from rest_framework import serializers
from .models import Product, Vehicle, VehicleProduct, VehicleSalesperson
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


class VehicleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleProduct
        exclude = ['vehicle_salesperson']


class AssignVehicleSalespersonSerializer(serializers.ModelSerializer):
    assigned_vehicle = VehicleProductSerializer(many=True)

    class Meta:
        model = VehicleSalesperson
        exclude = ['assigned_by']
        extra_fields = ['assigned_vehicle']

    def create(self, validated_data):
        product_data = validated_data.pop('assigned_vehicle')
        vehicleSp = VehicleSalesperson.objects.create(**validated_data)
        for item in product_data:
            VehicleProduct.objects.create(vehicle_salesperson=vehicleSp, **item)
        return vehicleSp


class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ['created_by']


class AssignedVehicleItemsSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()

    class Meta:
        model = VehicleProduct
        fields = ['product', 'quantity']


class SalespersonAssignedVehicleSerializer(serializers.ModelSerializer):
    vehicle = VehicleDetailSerializer()

    assigned_vehicle = AssignedVehicleItemsSerializer(many=True, )

    class Meta:
        model = VehicleSalesperson
        exclude = ['assigned_by']
        extra_fields = ['assigned_vehicle']

#GET all vehicles and assigned product/salesperson details
class VehicleListViewSerializer(serializers.ModelSerializer):
    assigned_salesperson = SalespersonDetailSerializer()

    assigned_products = AssignedVehicleItemsSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        extra_fields = ['assigned_products']
        model = Vehicle
