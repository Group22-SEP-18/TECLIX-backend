import decimal

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerViewSerializer, ServiceOrderViewSerializer, CreateServiceOrderSerializer, \
    CustomerSearchSerializer, CustomerLatePayListViewSerializer, CustomerLatePayCreateSerializer, \
    CustomerLatePayViewSerializer, LoyaltyPointsSerializer
from .models import Customer, ServiceOrder, CustomerLatePay, CustomerLoyaltyPointScheme
from rest_framework import filters
from users.permissions import IsSalesperson, IsManager
from salesperson_api.models import Leaderboard, LeaderboardPointSchema


# Create your views here.


class CustomerListView(ListCreateAPIView):
    serializer_class = CustomerViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        # get leaderboard obj
        lb_object = Leaderboard.objects.get(salesperson=self.request.user)

        # get the points from schema
        schema = LeaderboardPointSchema.objects.get(points_type='CUSTOMER_CREATION')

        # update leaderboard
        lb_object.points_today += schema.bonus_points
        lb_object.points_current_month += schema.bonus_points
        lb_object.points_all_time += schema.bonus_points
        lb_object.save()
        return serializer.save(created_by=self.request.user)


class CustomerView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()
    lookup_field = "id"


class ServiceOrderListView(ListAPIView):
    serializer_class = ServiceOrderViewSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        orders = ServiceOrder.objects.all()
        return orders


# view so by id
class ServiceOrderView(RetrieveAPIView):
    serializer_class = ServiceOrderViewSerializer
    permission_classes = (IsAuthenticated,)

    queryset = ServiceOrder.objects.all()
    lookup_field = "id"


#  view all so by customer
class CustomerServiceOrdersView(ListAPIView):
    serializer_class = ServiceOrderViewSerializer
    permission_classes = (IsAuthenticated,)

    # lookup_field = 'customer'

    def get_queryset(self):
        orders = ServiceOrder.objects.filter(customer_id=self.kwargs['id'])
        return orders


# create so view
class CreateServiceOrderView(CreateAPIView):
    serializer_class = CreateServiceOrderSerializer
    permission_classes = (IsAuthenticated, IsSalesperson)

    def perform_create(self, serializer):
        return serializer.save(salesperson=self.request.user)


# search customer view
class SearchCustomerView(ListAPIView):
    serializer_class = CustomerSearchSerializer
    queryset = Customer.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['shop_name', 'owner_first_name', 'owner_last_name']


# customer late payment related
class AllCustomerLatePayView(ListAPIView):
    serializer_class = CustomerLatePayListViewSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        payments = CustomerLatePay.objects.all()
        return payments


# post customer late pay
class CreateLatePayView(CreateAPIView):
    serializer_class = CustomerLatePayCreateSerializer
    permission_classes = (IsAuthenticated, IsSalesperson)

    def perform_create(self, serializer):
        cus = Customer.objects.get(id=self.request.data['customer'])
        cus.outstanding -= decimal.Decimal(self.request.data['amount'])
        cus.save()

        # get leaderboard obj
        lb_object = Leaderboard.objects.get(salesperson=self.request.user)

        # get the points from schema
        schema = LeaderboardPointSchema.objects.get(points_type='LATE_PAYMENTS')

        # update leaderboard
        points = schema.bonus_points + decimal.Decimal(
            self.request.data['amount']) * schema.percentage / 100
        lb_object.points_today += points
        lb_object.points_current_month += points
        lb_object.points_all_time += points
        lb_object.save()
        return serializer.save(salesperson=self.request.user)


# view late per customer
class CustomerLatePayView(ListAPIView):
    serializer_class = CustomerLatePayViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        payments = CustomerLatePay.objects.filter(customer_id=self.kwargs['id'])
        return payments


class CreateLoyaltyPointsView(CreateAPIView):
    serializer_class = LoyaltyPointsSerializer
    permission_classes = (IsAuthenticated, IsManager)

    def perform_create(self, serializer):
        return serializer.save()


class DeleteLoyaltyPointsView(DestroyAPIView):
    serializer_class = LoyaltyPointsSerializer
    permission_classes = (IsAuthenticated, IsManager)
    queryset = CustomerLoyaltyPointScheme.objects.all()
