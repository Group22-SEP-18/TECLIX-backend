from django.urls import path
from .views import GetMonthlySalespersonSalesView

urlpatterns = [
    path('salesperson/month/<int:sp>', GetMonthlySalespersonSalesView.as_view(), name='salesperson-month'),

]
