from rest_framework import generics, status
from .serializers import GetMonthlySalesSerializer
from customer_api.models import ServiceOrder
from rest_framework.response import Response


class GetMonthlySalespersonSalesView(generics.GenericAPIView):

    def get(self, request, sp, mon):
        so = ServiceOrder.objects.filter(order_date__month=mon, salesperson=sp)
        total_sales = 0
        for item in so:
            total_sales += item.original_price
        return Response({'salesperson': sp, 'total_sales': total_sales}, status=status.HTTP_200_OK)
