from rest_framework import serializers
from customer_api.models import ServiceOrder


class GetMonthlySalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ['salesperson', 'month', ]
