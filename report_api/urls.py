from django.urls import path
from .views import GetMonthlySalespersonSalesView

urlpatterns = [
    path('salesperson/month/<int:sp>/<int:mon>', GetMonthlySalespersonSalesView.as_view(), name='salesperson-month'),

]
