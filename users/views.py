from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes

from .serializers import RegisterStaffSerializer, LoginStaffSerializer, UserDetailSerializer, \
    ApproveAccSerializer
from .models import Staff
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView


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


class GetLoggedUserFromToken(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


# update salesperson approve state
class UpdateSalespersonAccStateView(generics.UpdateAPIView):
    serializer_class = ApproveAccSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Staff.objects.all()
    lookup_field = 'id'


class UpdateDistOfficerAccStateView(generics.UpdateAPIView):
    serializer_class = ApproveAccSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Staff.objects.all()
    lookup_field = 'id'
