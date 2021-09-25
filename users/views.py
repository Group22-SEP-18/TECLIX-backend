from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes

from .serializers import RegisterStaffSerializer, LoginWebStaffSerializer, UserDetailSerializer, \
    ApproveAccSerializer, LoginSalespersonSerializer
from .models import Staff
from rest_framework.response import Response
from knox.models import AuthToken
from .permissions import IsManager, IsOfficer
from .renderer import UserRenderer
from salesperson_api.models import Leaderboard


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
        if user.user_role == 'SALESPERSON':
            Leaderboard.objects.create(salesperson=user)

        token = AuthToken.objects.create(user)[1]

        # in case user data include password
        if 'password' in user_data:
            del user_data['password']

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginWebStaffView(generics.GenericAPIView):
    serializer_class = LoginWebStaffSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginSalespersonStaffView(generics.GenericAPIView):
    serializer_class = LoginSalespersonSerializer
    renderer_classes = (UserRenderer,)

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
    permission_classes = (permissions.IsAuthenticated, IsOfficer)
    queryset = Staff.objects.all()
    lookup_field = 'id'


class UpdateDistOfficerAccStateView(generics.UpdateAPIView):
    serializer_class = ApproveAccSerializer
    permission_classes = (permissions.IsAuthenticated, IsManager)
    queryset = Staff.objects.all()
    lookup_field = 'id'
