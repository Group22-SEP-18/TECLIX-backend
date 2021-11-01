from rest_framework import serializers
from users.models import Staff
from customer_api.models import Customer
from .models import SalespersonLocation, Leaderboard, LeaderboardPointSchema


class SalespersonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'email', 'employee_no', 'first_name', 'last_name', 'contact_no', 'profile_picture',
                  'is_approved', ]


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


class LeaderboardSalespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'employee_no', 'first_name', 'last_name', 'profile_picture']


class LeaderboardViewSerializer(serializers.ModelSerializer):
    salesperson = LeaderboardSalespersonSerializer()

    class Meta:
        model = Leaderboard
        exclude = ['id']


class LeaderboardPointSchemaViewSerializer(serializers.ModelSerializer):
    points_type = serializers.CharField(source='get_points_type_display')

    class Meta:
        model = LeaderboardPointSchema
        fields = '__all__'
