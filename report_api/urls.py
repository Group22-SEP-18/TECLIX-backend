from django.urls import path
from .views import GetMonthlySalespersonSalesView, GetTwoMonthComparisonSalesView

urlpatterns = [
    path('salesperson/month/<int:sp>', GetMonthlySalespersonSalesView.as_view(), name='salesperson-month'),
    path('salesperson/month-comparison/<int:sp>', GetTwoMonthComparisonSalesView.as_view(),
         name='salesperson-two-month'),

]
