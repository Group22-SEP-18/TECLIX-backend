from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RegisterStaffSerializer, LoginStaffSerializer
from .models import Staff
from rest_framework.response import Response
from knox.models import AuthToken


# Create your views here.
class RegisterStaffView(generics.GenericAPIView):
    serializer_class = RegisterStaffSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = Staff.objects.get(email=user_data['email'])

        token = AuthToken.objects.create(user)[1]

        # in case user data include password
        if 'password' in user_data:
            del user_data['password']

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginStaffView(generics.GenericAPIView):
    serializer_class = LoginStaffSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
