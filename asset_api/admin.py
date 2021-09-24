from django.contrib import admin
from .models import Product, Vehicle, VehicleProduct, VehicleSalesperson

# Register your models here.
admin.site.register(Product)
admin.site.register(Vehicle)
admin.site.register(VehicleProduct)
admin.site.register(VehicleSalesperson)
