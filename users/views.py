from rest_framework import generics, status, permissions
from rest_framework.decorators import permission_classes

from .serializers import RegisterStaffSerializer, LoginWebStaffSerializer, UserDetailSerializer, \
    ApproveAccSerializer, LoginSalespersonSerializer, DOAccountSerializer
from .models import Staff
from rest_framework.response import Response
from knox.models import AuthToken
from .permissions import IsManager, IsOfficer
from .renderer import UserRenderer
from salesperson_api.models import Leaderboard


# Create your views here.
class RegisterStaffView(generics.GenericAPIView):
    serializer_class = RegisterStaffSerializer
    renderer_classes = (UserRenderer,)

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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
class UpdateSalespersonAccStateView(generics.CreateAPIView):
    serializer_class = ApproveAccSerializer
    permission_classes = (permissions.IsAuthenticated, IsOfficer)
    queryset = Staff.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        sp = Staff.objects.get(id=self.kwargs['id']);
        print(self.kwargs['id'])
        if not self.request.data['is_approved']:
            sp.is_rejected = True
        sp.is_approved = self.request.data['is_approved']
        # create leaderboard entry
        if self.request.data['is_approved']:
            Leaderboard.objects.create(salesperson=sp)
        return sp.save()


class UpdateDistOfficerAccStateView(generics.CreateAPIView):
    serializer_class = ApproveAccSerializer
    permission_classes = (permissions.IsAuthenticated, IsManager)
    queryset = Staff.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        do = Staff.objects.get(id=self.kwargs['id']);
        print(self.kwargs['id'])
        if not self.request.data['is_approved']:
            do.is_rejected = True
        do.is_approved = self.request.data['is_approved']
        return do.save()


class GetDOAccountsView(generics.ListAPIView):
    serializer_class = DOAccountSerializer

    # permission_classes = (permissions.IsAuthenticated, IsManager)

    def get_queryset(self):
        return Staff.objects.filter(user_role='OFFICER', is_rejected=False)
