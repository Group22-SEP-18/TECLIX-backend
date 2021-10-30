from django.urls import path
from .views import GetMonthlySalespersonSalesView, GetSalespersonMonthlySales, GetDailyStatsView, \
    GetMonthlyComparison, GetCurrentMonthSalesForSalesPersons, GetSalespersonPerformanceComparisonView, \
    GetMonthlyTotalSales, GetMonthlyPayedAndPayLaterComparison, GetProductReport

app_name = 'report'

urlpatterns = [
    path('salesperson/month/<int:sp>', GetMonthlySalespersonSalesView.as_view(), name='salesperson-month'),
    path('salesperson/monthly-sales/<int:sp>', GetSalespersonMonthlySales.as_view(), name='salesperson-all-month'),
    path('salesperson/daily-stats/<int:sp>', GetDailyStatsView.as_view(), name='salesperson-daily'),
    path('salesperson/monthly-stat-comparison/<int:sp>', GetMonthlyComparison.as_view(),
        name='salesperson-monthly-comp'),
    path('salesperson-sales-current-month', GetCurrentMonthSalesForSalesPersons.as_view(),
        name='salesperson-sales-current-month'),
    path('salesperson-sales-progress', GetSalespersonPerformanceComparisonView.as_view(),
        name='salesperson-sales-progress'),
    path('total-sales-by-month', GetMonthlyTotalSales.as_view(),
        name='total-sales-by-month'),
    path('pay-and-pay-later', GetMonthlyPayedAndPayLaterComparison.as_view(),
        name='pay-and-pay-later'),
    path('sales-per-product', GetProductReport.as_view(),
        name='sales-per-product'),

]
