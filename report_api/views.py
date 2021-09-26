import datetime
from .serializers import GetMonthlySalesSerializer
from rest_framework import generics, status
from rest_framework import permissions
from customer_api.models import ServiceOrder, CustomerLatePay
from rest_framework.response import Response
from django.db.models import Sum


class GetMonthlySalespersonSalesView(generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
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

    def get(self, request, sp):
        results = ServiceOrder.objects.filter(salesperson=sp).values('order_date__month').annotate(
            sales=Sum('original_price')).order_by(
            'order_date__month')
        return Response(results, status=status.HTTP_200_OK)
