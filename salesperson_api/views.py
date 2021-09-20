from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from customer_api.serializers import ServiceOrderViewSerializer
from .serializers import SalespersonViewSerializer, LocationListViewSerializer
from users.models import Staff
from customer_api.models import ServiceOrder
from .models import SalespersonLocation


# Create your views here.
class SalespersonListView(ListAPIView):
    serializer_class = SalespersonViewSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        salespersons = Staff.objects.filter(user_role='SALESPERSON')
        return salespersons


class LocationListView(ListAPIView):
    serializer_class = LocationListViewSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = SalespersonLocation.objects.all()

class CurrentLocationListView(ListAPIView):
    serializer_class = LocationListViewSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_locations = SalespersonLocation.objects.all().order_by('salesperson', 'date').distinct('salesperson')
        return current_locations

class SalespersonLocationView(ListAPIView):
    serializer_class = LocationListViewSerializer
    # permission_classes = (IsAuthenticated,)
    # lookup_field = 'salesperson'

    def get_queryset(self):
        locations = SalespersonLocation.objects.filter(salesperson_id=self.kwargs['id'])
        return locations

class SalespersonServiceOrdersView(ListAPIView):
    serializer_class = ServiceOrderViewSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        orders = ServiceOrder.objects.filter(salesperson_id=self.kwargs['id'])
        return orders