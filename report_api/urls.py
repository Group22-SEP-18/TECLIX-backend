from django.urls import path
from .views import GetMonthlySalespersonSalesView, GetSalespersonMonthlySales, GetDailyStatsView, GetMonthlyComparison

app_name = 'report'

urlpatterns = [
    path('salesperson/month/<int:sp>', GetMonthlySalespersonSalesView.as_view(), name='salesperson-month'),
    path('salesperson/monthly-sales/<int:sp>', GetSalespersonMonthlySales.as_view(), name='salesperson-all-month'),
    path('salesperson/daily-stats/<int:sp>', GetDailyStatsView.as_view(), name='salesperson-daily'),
    path('salesperson/monthly-stat-comparison/<int:sp>', GetMonthlyComparison.as_view(),
         name='salesperson-monthly-comp'),

]
