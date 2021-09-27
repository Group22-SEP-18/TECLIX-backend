from django.db import models

# Create your models here.
from django.db import models
from users.models import Staff


class Product(models.Model):
    CATEGORY_OPTIONS = {
        ('biscuit', 'Biscuit'),
        ('chips', 'Chips'),
        ('cookies', 'Cookies'),
        ('cheese', 'Cheese'),
    }
    short_name = models.CharField(max_length=80)
    long_name = models.CharField(max_length=250)
    barcode = models.CharField(max_length=150, default='unknown', db_index=True, unique=True)
    product_image = models.ImageField(upload_to='product/', max_length=255, blank=True)
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)


class Vehicle(models.Model):
    VEHICLE_TYPES = {
        ('VAN', 'Van'),
        ('LORRY', 'Lorry'),
        ('THREEWHEELER', 'Threewheeler'),
        ('CAB', 'Cab'),
        ('BIKE', 'Bike'),
        ('BUS', 'Bus'),
    }
    vehicle_number = models.CharField(max_length=80)
    vehicle_type = models.CharField(choices=VEHICLE_TYPES, max_length=150)
    vehicle_image = models.ImageField(upload_to='vehicle/', max_length=255)
    vehicle_model = models.CharField(max_length=150)
    created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)


class VehicleSalesperson(models.Model):
    vehicle = models.ForeignKey(to=Vehicle, related_name='vehicle_items', on_delete=models.CASCADE, db_index=True)
    salesperson = models.ForeignKey(to=Staff, related_name='vehicle_salesperson', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(to=Staff, related_name='salesperson_assigner', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['vehicle', 'salesperson']
        ordering = ['vehicle']

    def __str__(self):
        return str(self.vehicle) + ' ' + str(self.salesperson)


class VehicleProduct(models.Model):
    vehicle_salesperson = models.ForeignKey(to=VehicleSalesperson, related_name='assigned_vehicle',
                                            on_delete=models.CASCADE,
                                            db_index=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='assigned_products')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ['vehicle_salesperson', 'product']
        ordering = ['vehicle_salesperson']

    def __str__(self):
        return str(self.vehicle_salesperson)
