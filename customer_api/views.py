import decimal

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerViewSerializer, ServiceOrderViewSerializer, CreateServiceOrderSerializer, \
    CustomerSearchSerializer, CustomerLatePayListViewSerializer, CustomerLatePayCreateSerializer, \
    CustomerLatePayViewSerializer
from .models import Customer, ServiceOrder, CustomerLatePay
from rest_framework import filters


# Create your views here.

class CustomerListView(ListCreateAPIView):
    serializer_class = CustomerViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(salesperson=self.request.user)


# search cutomer view
class SearchCustomerView(ListAPIView):
    serializer_class = CustomerSearchSerializer
    queryset = Customer.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['shop_name', 'owner_first_name', 'owner_last_name']


# customer late payment related
class AllCustomerLatePayView(ListAPIView):
    serializer_class = CustomerLatePayListViewSerializer

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        payments = CustomerLatePay.objects.all()
        return payments


# post customer late pay
class CreateLatePayView(CreateAPIView):
    serializer_class = CustomerLatePayCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        cus = Customer.objects.get(id=self.request.data['customer'])
        cus.outstanding -= decimal.Decimal(self.request.data['amount'])
        cus.save()
        return serializer.save(salesperson=self.request.user)


# view late per customer
class CustomerLatePayView(ListAPIView):
    serializer_class = CustomerLatePayViewSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        payments = CustomerLatePay.objects.filter(customer_id=self.kwargs['id'])
        return payments
