from rest_framework import serializers
from .models import Staff


class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=48, min_length=6, write_only=True)

    class Meta:
        model = Staff
        fields = ['email', 'password', 'user_role', 'first_name', 'last_name', 'contact_no', 'profile_picture']

    def validate(self, attrs):
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        contact_no = attrs.get('contact_no', '')

        if not first_name.isalpha():
            raise serializers.ValidationError("The first name should only contain letters")

        if not last_name.isalpha():
            raise serializers.ValidationError("The last name should only contain letters")

        if not contact_no.isdigit():
            raise serializers.ValidationError("the contact number should only contain numbers.")
        if not len(contact_no) == 10:
            raise serializers.ValidationError("the contact number must be 10 digits long.")
        return attrs

    def create(self, validated_data):
        return Staff.objects.create_user(**validated_data)
