from .views import SalespersonListView, LocationListView, CurrentLocationListView
from django.urls import path

urlpatterns = [
    path('', SalespersonListView.as_view(), name='all-salespersons'),
    path('locations/', LocationListView.as_view(), name='all-locations'),
    path('locations/current', CurrentLocationListView.as_view(), name='current-locations'),
]