from rest_framework import serializers
from customer_api.models import ServiceOrder


class GetMonthlySalesSerializer(serializers.ModelSerializer):
    month = serializers.IntegerField()

    class Meta:
        model = ServiceOrder
        fields = ['salesperson', 'month']
