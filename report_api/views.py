import datetime
import decimal

from django.db.models.functions import Coalesce
from django.db.models import DecimalField, FloatField

from .serializers import GetMonthlySalesSerializer, GetSalesSerializer, GetMonthlyTotalSalesSerializer
from rest_framework import generics, status
from rest_framework import permissions
from customer_api.models import ServiceOrder, CustomerLatePay, Customer
from rest_framework.response import Response
from django.db.models import Sum, Count
from users.models import Staff


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


# object in array for each salesperson for current month
# [
#   {
#     salesperson: 'salesperson',
#     sales: 000.00,
#   }
# ] 
class GetCurrentMonthSalesForSalesPersons(generics.GenericAPIView):
    serializer_class = GetSalesSerializer

    def get(self, request):
        this_month = datetime.date.today().month
        results = ServiceOrder.objects.filter(order_date__month=this_month,
                                              order_date__year=datetime.date.today().year).values(
            'salesperson').annotate(
            sales=Sum('original_price'))

        for val in results:
            sp = Staff.objects.get(id=val['salesperson'])
            val['salesperson'] = sp.first_name + ' ' + sp.last_name

        return Response(results, status=status.HTTP_200_OK)


# Compare last two months and show, growth per salesperson (double column bar chart)
# response - object in array for each month
# [
#   {
#     salesperson: 'salesperson',
#     sales_last_month: 000.00,
#     sales_current_month: 000.00,
#   }
# ]
class GetSalespersonPerformanceComparisonView(generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetSalesSerializer

    def get(self, request):
        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)

        sp_list = Staff.objects.filter(is_approved=True, user_role='SALESPERSON')
        result = []
        for sp in sp_list:
            cur = ServiceOrder.objects.filter(order_date__month=datetime.date.today().month,
                                              order_date__year=datetime.date.today().year,
                                              salesperson=sp.id).values('salesperson').annotate(
                sales_current_month=Coalesce(Sum('original_price', output_field=FloatField()), float(0.00)))

            try:
                cur_value = cur[0]['sales_current_month']
            except:
                cur_value = 0.0

            pre = ServiceOrder.objects.filter(order_date__month=last_month.month,
                                              order_date__year=last_month.year,
                                              salesperson=sp.id).values('salesperson').annotate(
                sales_last_month=Coalesce(Sum('original_price', output_field=FloatField()), float(0.00)))

            try:
                pre_value = pre[0]['sales_last_month']
            except:
                pre_value = 0.0

            result.append({'salesperson': sp.first_name + ' ' + sp.last_name, 'sales_current_month': cur_value,
                           'sales_last_month': pre_value})
        return Response(result, status=status.HTTP_200_OK)


# Total sales line chart
# response - object in array for each month
# [
#   {
#     month: 'month',
#     sales: 000.00
#   }
# ]
class GetMonthlyTotalSales(generics.GenericAPIView):
    serializer_class = GetMonthlyTotalSalesSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        results = ServiceOrder.objects.all().values('order_date__month').annotate(
            sales=Sum('original_price')).order_by(
            'order_date__month')
        return Response(results, status=status.HTTP_200_OK)


# Divided bar chart per day sales one half paid another half later And a pie chart illustrating that.
# response - object for each day in the current month
# [
#   {
#     day: '01',
#     paid_amount: 000.00,
#     pay_later_amount: 000.00,
#   }
# ]
class GetMonthlyPayedAndPayLaterComparison(generics.GenericAPIView):
    # TODO:
    pass


# sales per product by month
# [
#   {
#     product_id: 'product id',
#     product_short_name: 'product name',
#     product_long_name: 'product name',
#     total: 000.00,
#     date: '2021-06-22T17:33:34Z',
#   }
# ]
class GetProductReport(generics.GenericAPIView):
    # TODO:
    pass
