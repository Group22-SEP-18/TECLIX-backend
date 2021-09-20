from .views import SalespersonListView, LocationListView, CurrentLocationListView, SalespersonLocationView
from django.urls import path

urlpatterns = [
    path('', SalespersonListView.as_view(), name='all-salespersons'),
    path('locations/', LocationListView.as_view(), name='all-locations'),
    path('locations/current', CurrentLocationListView.as_view(), name='all-salesperson-locations'),
    path('locations/<str:id>', SalespersonLocationView.as_view(), name='all-locations'),
]