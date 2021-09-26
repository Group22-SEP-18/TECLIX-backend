import datetime

from rest_framework import generics, status
from .serializers import GetMonthlySalesSerializer
from customer_api.models import ServiceOrder
from rest_framework.response import Response


class GetMonthlySalespersonSalesView(generics.GenericAPIView):

    def get(self, request, sp):
        so = ServiceOrder.objects.filter(order_date__month=datetime.date.today().month, salesperson=sp,
                                         order_date__year=datetime.date.today().year)
        total_sales = 0
        for item in so:
            total_sales += item.original_price
        return Response({'salesperson': sp, 'total_sales': total_sales}, status=status.HTTP_200_OK)


class GetTwoMonthComparisonSalesView(generics.GenericAPIView):

    def get(self, request, sp):
        if datetime.date.today().month == 1:
            prev_month = 12
            prev_month_year = datetime.date.today().year - 1
        else:
            prev_month = datetime.date.today().month - 1
            prev_month_year = datetime.date.today().year
        so = ServiceOrder.objects.filter(order_date__month=datetime.date.today().month, salesperson=sp,
                                         order_date__year=datetime.date.today().year)
        prev_so = ServiceOrder.objects.filter(order_date__month=prev_month, salesperson=sp,
                                              order_date__year=prev_month_year)
        cur_sales = 0
        prev_sales = 0

        for i in so:
            cur_sales += i.original_price

        for j in prev_so:
            prev_sales += j.original_price
        return Response({'salesperson': sp, 'sales_current_month': cur_sales, 'sales_last_month': prev_sales},
                        status=status.HTTP_200_OK)
