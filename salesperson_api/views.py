from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SalespersonViewSerializer, LocationListViewSerializer
from users.models import Staff
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

