import datetime
import decimal

from django.db.models.functions import Coalesce

from .serializers import GetMonthlySalesSerializer
from rest_framework import generics, status
from rest_framework import permissions
from customer_api.models import ServiceOrder, CustomerLatePay, Customer
from rest_framework.response import Response
from django.db.models import Sum, Count


class GetMonthlySalespersonSalesView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetMonthlySalesSerializer

    def get(self, request, sp):
        total_sales = ServiceOrder.objects.filter(order_date__month=datetime.date.today().month, salesperson=sp,
                                                  order_date__year=datetime.date.today().year).aggregate(
            Sum('original_price'))
        total_late_pay = CustomerLatePay.objects.filter(date__month=datetime.date.today().month, salesperson=sp,
                                                        date__year=datetime.date.today().year).aggregate(
            Sum('amount'))

        return Response({'salesperson': sp, 'total_sales': total_sales['original_price__sum'],
                         'total_late_pay': total_late_pay['amount__sum']},
                        status=status.HTTP_200_OK)


class GetSalespersonMonthlySales(generics.GenericAPIView):
    serializer_class = GetMonthlySalesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, sp):
        results = ServiceOrder.objects.filter(salesperson=sp).values('order_date__month').annotate(
            sales=Sum('original_price')).order_by(
            'order_date__month')
        return Response(results, status=status.HTTP_200_OK)


class GetDailyStatsView(generics.GenericAPIView):
    serializer_class = GetMonthlySalesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, sp):
        results = ServiceOrder.objects.filter(salesperson=sp, order_date__day=datetime.date.today().day,
                                              order_date__month=datetime.date.today().month,
                                              order_date__year=datetime.date.today().year).aggregate(
            total_sales=Coalesce(Sum('original_price'), decimal.Decimal(0.0)), shops=Count('id'))
        results2 = CustomerLatePay.objects.filter(salesperson=sp, date__day=datetime.date.today().day,
                                                  date__month=datetime.date.today().month,
                                                  date__year=datetime.date.today().year).aggregate(
            pay_count=Count('id'))

        results['shops'] += results2['pay_count']

        return Response({**results, **results2}, status=status.HTTP_200_OK)


class GetMonthlyComparison(generics.GenericAPIView):
    serializer_class = GetMonthlySalesSerializer

    def get(self, request, sp):
        results = ServiceOrder.objects.filter(salesperson=sp, order_date__month=datetime.date.today().month,
                                              order_date__year=datetime.date.today().year).aggregate(
            so_count=Count('id'))
        results2 = CustomerLatePay.objects.filter(salesperson=sp, date__month=datetime.date.today().month,
                                                  date__year=datetime.date.today().year).aggregate(
            pay_count=Count('id'))
        result3 = Customer.objects.filter(created_by=sp, created_date__month=datetime.date.today().month,
                                          created_date__year=datetime.date.today().year).aggregate(
            customer_count=Count('id'))
        return Response({**results, **results2, **result3}, status=status.HTTP_200_OK)
