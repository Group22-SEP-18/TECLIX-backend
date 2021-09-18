from rest_framework import serializers
from .models import Customer


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
