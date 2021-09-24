from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductDetailsSerializer, ProductViewSerializer, VehicleDetailsSerializer, \
    VehicleViewSerializer, AssignVehicleProductSerializer, AssignVehicleSalespersonSerializer
from .models import Product, Vehicle
from users.permissions import IsOfficer


# Create a product POST, GET all products
class ProductListView(ListCreateAPIView):
    serializer_class = ProductDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)


# Single product GET, PUT, DELETE
class ProductView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    lookup_field = "id"


# Create a vehicle POST
class VehicleCreateView(CreateAPIView):
    serializer_class = VehicleDetailsSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Vehicle.objects.all()

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)


# Single vehicle GET, PUT, DELETE
class VehicleView(RetrieveUpdateDestroyAPIView):
    serializer_class = VehicleViewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Vehicle.objects.all()
    lookup_field = "id"


# GET all vehicle details
class VehicleListView(ListAPIView):
    serializer_class = VehicleViewSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        vehicle = Vehicle.objects.all()
        return vehicle


class AssignVehicleProductsView(CreateAPIView):
    serializer_class = AssignVehicleProductSerializer

    permission_classes = (IsAuthenticated, IsOfficer)

    def perform_create(self, serializer):
        return serializer.save(assigned_by=self.request.user)


class AssignVehicleSalespersonView(CreateAPIView):
    serializer_class = AssignVehicleSalespersonSerializer

    permission_classes = (IsAuthenticated, IsOfficer)

    def perform_create(self, serializer):
        return serializer.save(assigned_by=self.request.user)
