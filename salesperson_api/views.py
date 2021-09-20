from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SalespersonViewSerializer
from .models import Staff


# Create your views here.
class SalespersonListView(ListAPIView):
    serializer_class = SalespersonViewSerializer

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        salespersons = Staff.objects.filter(user_role='SALESPERSON')
        return salespersons


