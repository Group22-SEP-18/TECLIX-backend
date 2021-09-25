from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from customer_api.serializers import ServiceOrderViewSerializer
from .serializers import SalespersonViewSerializer, LocationListViewSerializer, LeaderboardViewSerializer, \
    LeaderboardPointSchemaViewSerializer
from users.models import Staff
from customer_api.models import ServiceOrder
from .models import SalespersonLocation, Leaderboard, LeaderboardPointSchema


# Create your views here.
class SalespersonListView(ListAPIView):
    serializer_class = SalespersonViewSerializer

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        salespersons = Staff.objects.filter(user_role='SALESPERSON')
        return salespersons


class SalespersonView(RetrieveUpdateAPIView):
    serializer_class = SalespersonViewSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = Staff.objects.filter()
    lookup_field = "id"


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


class LeaderboardView(ListAPIView):
    serializer_class = LeaderboardViewSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = Leaderboard.objects.all().order_by('-points_current_month')[:10]


class LeaderboardPointSchemaView(ListCreateAPIView):
    serializer_class = LeaderboardPointSchemaViewSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = LeaderboardPointSchema.objects.all()
