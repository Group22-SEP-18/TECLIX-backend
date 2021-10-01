from rest_framework import serializers
from .models import Staff
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=48, min_length=6, write_only=True)

    class Meta:
        model = Staff
        fields = ['email', 'employee_no', 'password', 'user_role', 'first_name', 'last_name', 'contact_no',
                  'profile_picture']

    def validate(self, attrs):
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        contact_no = attrs.get('contact_no', '')
        employee_no = attrs.get('employee_no', '')
        if not first_name.isalpha():
            raise serializers.ValidationError("The first name should only contain letters")

        if not last_name.isalpha():
            raise serializers.ValidationError("The last name should only contain letters")

        if not contact_no.isdigit():
            raise serializers.ValidationError("the contact number should only contain numbers.")
        if not len(contact_no) == 10:
            raise serializers.ValidationError("the contact number must be 10 digits long.")
        if not contact_no.isalnum():
            raise serializers.ValidationError("the contact number should only contain  alpha numeric characters.")
        return attrs

    def create(self, validated_data):
        return Staff.objects.create_user(**validated_data)


class LoginWebStaffSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225, min_length=3)
    password = serializers.CharField(max_length=48, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=225, read_only=True)
    last_name = serializers.CharField(max_length=225, read_only=True)
    employee_no = serializers.CharField(max_length=10, read_only=True)
    token = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(read_only=True)
    user_role = serializers.CharField(read_only=True)

    user = None

    def __init__(self, *args, **kwargs):
        super(LoginWebStaffSerializer, self).__init__(*args, **kwargs)
        try:
            self.user = Staff.objects.get(email=kwargs['data']['email'])
        except:
            pass

    def get_token(self, obj):
        return self.user.token()

    class Meta:
        model = Staff
        fields = ['id', 'employee_no', 'email', 'password', 'first_name', 'last_name', 'token', 'profile_picture',
                  'user_role']

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
        if user.user_role == 'SALESPERSON':
            raise AuthenticationFailed('You are not authorized to use the application.')

        return {
            'employee_no': user.employee_no,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': user.token,
            'profile_picture': user.profile_picture,
            'user_role': user.user_role,
            'id': user.id,

        }


# serializer for the salesperson login
class LoginSalespersonSerializer(serializers.ModelSerializer):
    # staff_id = serializers.IntegerField()
    email = serializers.EmailField(max_length=225, min_length=3)
    password = serializers.CharField(max_length=48, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=225, read_only=True)
    last_name = serializers.CharField(max_length=225, read_only=True)
    employee_no = serializers.CharField(max_length=10, read_only=True)
    token = serializers.SerializerMethodField()
    profile_picture = serializers.ImageField(read_only=True)
    contact_no = serializers.CharField(max_length=10, read_only=True)

    user = None

    def __init__(self, *args, **kwargs):
        super(LoginSalespersonSerializer, self).__init__(*args, **kwargs)
        try:
            self.user = Staff.objects.get(email=kwargs['data']['email'])
        except:
            pass

    def get_token(self, obj):
        return self.user.token()

    class Meta:
        model = Staff
        fields = ['id', 'employee_no', 'email', 'password', 'first_name', 'last_name', 'token', 'profile_picture',
                  'contact_no']

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
        if user.user_role != 'SALESPERSON':
            raise AuthenticationFailed('You are not authorized to use the application.')
        return {
            'employee_no': user.employee_no,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': user.token,
            'profile_picture': user.profile_picture,
            'contact_no': user.contact_no,
            'id': user.id,

        }


# this is used to get details of a user who is logged in
class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=225, min_length=3, read_only=True)
    first_name = serializers.CharField(max_length=225, read_only=True)
    last_name = serializers.CharField(max_length=225, read_only=True)
    employee_no = serializers.CharField(max_length=10, read_only=True)
    profile_picture = serializers.ImageField(read_only=True)

    class Meta:
        model = Staff
        fields = ['employee_no', 'email', 'first_name', 'last_name', 'token', 'profile_picture', 'user_role']


# this to specify what attrs required in the service order list

class SalespersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['employee_no', 'email', 'first_name', 'last_name', 'profile_picture']


#  approve salesperson accounts
class ApproveAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['is_approved']


# distribution officer serializer
class DOAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'employee_no', 'email', 'first_name', 'last_name', 'contact_no', 'profile_picture', 'is_rejected', 'is_approved']
