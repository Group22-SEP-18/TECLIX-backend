from django.db import models
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
    profile_picture = models.ImageField(upload_to='customer/', max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(choices=DISTRICT_OPTIONS, max_length=100)
    loyalty_points = models.DecimalField(max_digits=8, decimal_places=2)
    outstanding = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)


class ServiceOrder(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(to=Staff, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.id)


class OrderProduct(models.Model):
    order = models.ForeignKey(to=ServiceOrder, related_name='order_items', on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

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
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
