from .views import ProductListView, ProductView, VehicleCreateView, VehicleView, VehicleListView, \
    AssignVehicleItemsView, AssignedProductsListVehicleView, AllAssignedProductsListVehicleView
from django.urls import path

app_name = 'asset'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='all-products'),
    path('products/<int:id>', ProductView.as_view(), name='single-product'),
    path('vehicles/', VehicleListView.as_view(), name='all-vehicles'),
    path('vehicles/create', VehicleCreateView.as_view(), name='create-vehicle'),
    path('vehicles/<int:id>', VehicleView.as_view(), name='single-vehicle'),
    path('vehicle/assign-items/', AssignVehicleItemsView.as_view(), name='assign-vehicle-items'),
    path('vehicle/salesperson/', AssignedProductsListVehicleView.as_view(), name='get-vehicle-items'),
    path('vehicle/salesperson/all', AllAssignedProductsListVehicleView.as_view(), name='all-vehicle-items'),

]
