from rest_framework import serializers
from .models import Customer, ServiceOrder, OrderProduct
from users.serializers import ServiceOrderSalespersonSerializer
from asset_api.serializers import ProductDetailsSerializer


class CustomerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['created_by']

    def validate(self, attrs):
        contact_no = attrs.get('contact_no', '')

        if len(contact_no) < 10:
            raise serializers.ValidationError('The contact number is invalid')
        return attrs


# this to specify what attrs required in the service order list
class ServiceOrderCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['shop_name', 'owner_first_name', 'owner_last_name', 'profile_picture', ]


class OrderProductItemSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class ServiceOrderViewSerializer(serializers.ModelSerializer):
    customer = ServiceOrderCustomerSerializer()
    salesperson = ServiceOrderSalespersonSerializer()

    order_items = OrderProductItemSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        extra_fields = ['order_items']
        model = ServiceOrder
        # this will automatically resolve all the onetoone fields
        # depth = 1


# serializers to create so
class OrderProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        exclude = ['order']


class CreateServiceOrderSerializer(serializers.ModelSerializer):
    order_items = OrderProductCreateSerializer(many=True)

    class Meta:
        model = ServiceOrder
        exclude = ['salesperson']
        extra_fields = ['order_items']

    def create(self, validated_data):
        order_data = validated_data.pop('order_items')
        so = ServiceOrder.objects.create(**validated_data)
        for item in order_data:
            OrderProduct.objects.create(order=so, **item)
        return so


# customer search serializer

class CustomerSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['created_by']
