from .views import CustomerListView, CustomerView, ServiceOrderListView, ServiceOrderView, CustomerServiceOrdersView, \
    CreateServiceOrderView, SearchCustomerView, CustomerLatePayView
from django.urls import path

urlpatterns = [
    path('', CustomerListView.as_view(), name='all-customers'),
    path('<int:id>', CustomerView.as_view(), name='single-customer'),
    path('search/', SearchCustomerView.as_view(), name='search-customer'),
    path('service-orders/', ServiceOrderListView.as_view(), name='all-so'),
    path('service-orders/create', CreateServiceOrderView.as_view(), name='create-so'),
    path('service-orders/<int:id>', ServiceOrderView.as_view(), name='get-so'),
    path('service-orders/cus/<int:id>', CustomerServiceOrdersView.as_view(), name='all-customer-so'),
    path('late-payment/', CustomerLatePayView.as_view(), name='all-late-pay'),

]
