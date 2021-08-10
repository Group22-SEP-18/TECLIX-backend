from rest_framework import serializers
from .models import Staff
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


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


class LoginStaffSerializer(serializers.ModelSerializer):
    # staff_id = serializers.IntegerField()
    email = serializers.EmailField(max_length=225, min_length=3)
    password = serializers.CharField(max_length=48, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=225, read_only=True)
    last_name = serializers.CharField(max_length=225, read_only=True)
    token = serializers.SerializerMethodField()

    user = None

    def __init__(self, *args, **kwargs):
        super(LoginStaffSerializer, self).__init__(*args, **kwargs)
        try:
            self.user = Staff.objects.get(email=kwargs['data']['email'])
        except:
            pass

    def get_token(self, obj):
        return self.user.token()

    class Meta:
        model = Staff
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'token']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_approved:
            raise AuthenticationFailed('Your account is not approved.')
        if not user.is_active:
            raise AuthenticationFailed('Your account is disabled.')

        return {
            'staff_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': user.token

        }
