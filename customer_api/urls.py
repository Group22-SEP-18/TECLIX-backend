from .views import CustomerListView, CustomerView, ServiceOrderListView
from django.urls import path

urlpatterns = [
    path('', CustomerListView.as_view(), name='all-customers'),
    path('<int:id>', CustomerView.as_view(), name='single-customer'),
    path('service-orders/', ServiceOrderListView.as_view(), name='all-so'),

]
