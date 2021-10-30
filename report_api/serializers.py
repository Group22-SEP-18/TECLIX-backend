from rest_framework import serializers
from customer_api.models import ServiceOrder
from users.serializers import SalespersonDetailSerializer


class GetMonthlySalesSerializer(serializers.ModelSerializer):
    month = serializers.IntegerField()

    class Meta:
        model = ServiceOrder
        fields = ['salesperson', 'month']


class GetSalesSerializer(serializers.ModelSerializer):
    salesperson = SalespersonDetailSerializer()
    month = serializers.IntegerField()

    class Meta:
        model = ServiceOrder
        fields = ['salesperson', 'month']


class GetMonthlyTotalSalesSerializer(serializers.ModelSerializer):
    month = serializers.IntegerField()

    class Meta:
        model = ServiceOrder
        fields = ['month']
