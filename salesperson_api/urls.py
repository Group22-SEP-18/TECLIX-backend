from .views import SalespersonListView, SalespersonView, LocationListView, CurrentLocationListView, SalespersonLocationView, SalespersonServiceOrdersView
from django.urls import path

urlpatterns = [
    path('', SalespersonListView.as_view(), name='all-salespersons'),
    path('<str:id>', SalespersonView.as_view(), name='single-salesperson'),
    path('locations/', LocationListView.as_view(), name='all-locations'),
    path('locations/current', CurrentLocationListView.as_view(), name='all-salesperson-locations'),
    path('locations/<str:id>', SalespersonLocationView.as_view(), name='all-locations'),
    path('service-orders/salesperson/<str:id>', SalespersonServiceOrdersView.as_view(), name='all-salesperson-so'),
]