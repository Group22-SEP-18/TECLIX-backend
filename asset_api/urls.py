from .views import ProductListView, ProductView, VehicleCreateView, VehicleView, VehicleListView, \
    AssignVehicleProductsView, AssignVehicleSalespersonView
from django.urls import path

urlpatterns = [
    path('products/', ProductListView.as_view(), name='all-products'),
    path('products/<int:id>', ProductView.as_view(), name='single-product'),
    path('vehicles/', VehicleListView.as_view(), name='all-vehicles'),
    path('vehicles/create', VehicleCreateView.as_view(), name='create-vehicle'),
    path('vehicles/<int:id>', VehicleView.as_view(), name='single-vehicle'),
    path('vehicle/assign-product/', AssignVehicleProductsView.as_view(), name='assign-vehicle-product'),
    path('vehicle/assign-salesperson/', AssignVehicleSalespersonView.as_view(), name='assign-sp'),

]
