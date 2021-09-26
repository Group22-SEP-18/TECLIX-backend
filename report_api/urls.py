from django.urls import path
from .views import GetMonthlySalespersonSalesView, GetSalespersonMonthlySales

urlpatterns = [
    path('salesperson/month/<int:sp>', GetMonthlySalespersonSalesView.as_view(), name='salesperson-month'),
    path('salesperson/monthly-sales/<int:sp>', GetSalespersonMonthlySales.as_view(), name='salesperson-all-month'),

]
