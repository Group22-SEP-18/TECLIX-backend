from rest_framework import serializers
from users.models import Staff


class SalespersonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['email', 'employee_no', 'first_name', 'last_name', 'contact_no', 'profile_picture', 'is_approved', ]




