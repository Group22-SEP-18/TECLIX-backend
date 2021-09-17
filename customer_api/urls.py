from .views import CustomerListView, CustomerView
from django.urls import path

urlpatterns = [
    path('', CustomerListView.as_view(), name='all-customers'),
    path('<int:id>', CustomerView.as_view(), name='single-customer'),

]
