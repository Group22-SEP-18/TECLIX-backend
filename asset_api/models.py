from django.db import models

# Create your models here.
from django.db import models


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

    def __str__(self):
        return str(self.id)
