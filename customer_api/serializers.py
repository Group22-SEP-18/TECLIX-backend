from rest_framework import serializers
from .models import Customer, ServiceOrder
from users.serializers import ServiceOrderSalespersonSerializer


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


class ServiceOrderViewSerializer(serializers.ModelSerializer):
    customer = ServiceOrderCustomerSerializer()
    salesperson = ServiceOrderSalespersonSerializer()

    class Meta:
        fields = '__all__'
        model = ServiceOrder
        depth = 1
