from .views import SalespersonListView
from django.urls import path

urlpatterns = [
    path('', SalespersonListView.as_view(), name='all-salespersons'),
]