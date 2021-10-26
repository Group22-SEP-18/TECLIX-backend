from _cffi_backend import Lib
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductDetailsSerializer, ProductViewSerializer, VehicleDetailsSerializer, \
    VehicleViewSerializer, AssignVehicleSalespersonSerializer, \
    SalespersonAssignedVehicleSerializer, DeleteAssignedVehicleSerializer
from .models import Product, Vehicle, VehicleSalesperson, VehicleProduct
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

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        vehicle = Vehicle.objects.all()
        return vehicle


class AssignVehicleItemsView(CreateAPIView):
    serializer_class = AssignVehicleSalespersonSerializer

    permission_classes = (IsAuthenticated, IsOfficer)

    def perform_create(self, serializer):
        return serializer.save(assigned_by=self.request.user)


class AssignedProductsListVehicleView(ListAPIView):
    serializer_class = SalespersonAssignedVehicleSerializer
    permission_classes = (IsAuthenticated,)

    # lookup_field = "id"
    def get_queryset(self):
        return VehicleSalesperson.objects.filter(salesperson=self.request.user, is_valid=True)


class AllAssignedProductsListVehicleView(ListAPIView):
    serializer_class = SalespersonAssignedVehicleSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return VehicleSalesperson.objects.filter(is_valid=True)


class DeleteAssignedVehicle(DestroyAPIView):
    serializer_class = DeleteAssignedVehicleSerializer
    permission_classes = (IsAuthenticated, IsOfficer,)
    lookup_field = 'id'

    def get_queryset(self):
        print(self.kwargs['id'])
        return VehicleSalesperson.objects.filter(id=self.kwargs['id'], is_valid=True)
