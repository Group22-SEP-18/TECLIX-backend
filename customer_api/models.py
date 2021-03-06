from django.db import models
from django.utils.dateformat import DateFormat

from users.models import Staff
from asset_api.models import Product


# Create your models here.
class Customer(models.Model):
    DISTRICT_OPTIONS = {
        ('Ampara', 'Ampara'),
        ('Anuradhapura', 'Anuradhapura'),
        ('Badulla', 'Badulla'),
        ('Batticaloa', 'Batticaloa'),
        ('Colombo', 'Colombo'),
        ('Galle', 'Galle'),
        ('Gampaha', 'Gampaha'),
        ('Hambantota', 'Hambantota'),
        ('Jaffna', 'Jaffna'),
        ('Kalutara', 'Kalutara'),
        ('Kandy', 'Kandy'),
        ('Kegalle', 'Kegalle'),
        ('Kilinochchi', 'Kilinochchi'),
        ('Kurunegala', 'Kurunegala'),
        ('Mannar', 'Mannar'),
        ('Matale', 'Matale'),
        ('Matara', 'Matara'),
        ('Monaragala', 'Monaragala'),
        ('Mullaitivu', 'Mullaitivu'),
        ('Nuwara Eliya', 'Nuwara Eliya'),
        ('Polonnaruwa', 'Polonnaruwa'),
        ('Puttalam', 'Puttalam'),
        ('Ratnapura', 'Ratnapura'),
        ('Trincomalee', 'Trincomalee'),
        ('Vavuniya', 'Vavuniya')
    }
    shop_name = models.CharField(max_length=225, db_index=True)
    owner_first_name = models.CharField(max_length=100)
    owner_last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    contact_no = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='customer/', max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(choices=DISTRICT_OPTIONS, max_length=100)
    loyalty_points = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    outstanding = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ServiceOrder(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(to=Staff, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id)


class OrderProduct(models.Model):
    order = models.ForeignKey(to=ServiceOrder, related_name='order_items', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='product_details')
    quantity = models.PositiveIntegerField()
    price_at_the_time = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ['order', 'product']
        ordering = ['order']

    def __str__(self):
        return str(self.order)


class CustomerLatePay(models.Model):
    customer = models.ForeignKey(to=Customer, related_name='late_pay_customer', on_delete=models.CASCADE, db_index=True)
    salesperson = models.ForeignKey(to=Staff, related_name='late_pay_sp', on_delete=models.CASCADE,
                                    db_index=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class CustomerLoyaltyPointScheme(models.Model):
    POINTS_TYPE_OPTIONS = {
        ('LATE_PAYMENTS', 'Late Payments'),
        ('SO_PAY', 'SO payed'),
        ('SO_PAY_LATER', 'SO pay later'),
    }
    points_type = models.CharField(choices=POINTS_TYPE_OPTIONS, max_length=100, default='LATE_PAYMENTS')
    percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    bonus_points = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
