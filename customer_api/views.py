from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerViewSerializer, ServiceOrderViewSerializer
from .models import Customer, ServiceOrder


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
        orders = ServiceOrder.objects.select_related('customer')
        return orders
