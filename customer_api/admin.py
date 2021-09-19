from django.contrib import admin
from .models import Customer, ServiceOrder, OrderProduct, CustomerLatePay

# Register your models here.
admin.site.register(Customer)
admin.site.register(ServiceOrder)
admin.site.register(OrderProduct)
admin.site.register(CustomerLatePay)
