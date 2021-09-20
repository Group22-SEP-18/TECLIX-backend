from .views import SalespersonListView, LocationListView
from django.urls import path

urlpatterns = [
    path('', SalespersonListView.as_view(), name='all-salespersons'),
    path('locations/', LocationListView.as_view(), name='all-locations')
]