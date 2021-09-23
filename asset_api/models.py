from django.db import models

# Create your models here.
from django.db import models
from users.models import Staff


class Product(models.Model):
    CATEGORY_OPTIONS = {
        ('biscuit', 'Biscuit'),
        ('cake', 'Cake'),
    }
    short_name = models.CharField(max_length=80)
    long_name = models.CharField(max_length=250)
    product_image = models.ImageField(upload_to='product/', max_length=255)
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return str(self.id)

class Vehicle(models.Model):
    VEHICLE_TYPES = {
        ('VAN', 'Van'),
        ('LORRY', 'Lorry'),
        ('THREEWHEELER', 'threewheeler'),
        ('CAB', 'cab'),
        ('BIKE', 'bike'),
    }
    vehicle_number = models.CharField(max_length=80)
    vehicle_type = models.CharField(choices=VEHICLE_TYPES, max_length=150)
    vehicle_image = models.ImageField(upload_to='vehicle/', max_length=255)
    vehicle_model = models.CharField(max_length=150)
    created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)

class VehicleProduct(models.Model):
    vehicle = models.ForeignKey(to=Vehicle, related_name='assigned_vehicle', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='assigned_products')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ['vehicle', 'product']
        ordering = ['vehicle']

    def __str__(self):
        return str(self.vehicle)

# class VehicleSalesperson(models.Model):
#     vehicle = models.ForeignKey(to=Vehicle, name='assigned_vehicle', on_delete=models.CASCADE, db_index=True)
#     salesperson = models.ForeignKey(to=Product, on_delete=models.CASCADE, name='assigned_products')
#     date = models.DateField(auto_now_add=True)
#     created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         unique_together = ['vehicle', 'salesperson']
#         ordering = ['vehicle']

#     def __str__(self):
#         return str(self.vehicle)
