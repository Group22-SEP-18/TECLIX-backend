from rest_framework import serializers
from users.models import Staff
from customer_api.models import Customer
from .models import SalespersonLocation


class SalespersonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['email', 'employee_no', 'first_name', 'last_name', 'contact_no', 'profile_picture', 'is_approved', ]

class CustomerLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['latitude', 'longitude', 'street', 'city', 'district']

class LocationListViewSerializer(serializers.ModelSerializer):
    customer = CustomerLocationSerializer()
    salesperson = SalespersonViewSerializer()
    class Meta:
        model = SalespersonLocation
        fields = '__all__'