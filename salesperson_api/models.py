from django.db import models
from users.models import Staff
from customer_api.models import Customer


# Create your models here.
class SalespersonLocation(models.Model):
    salesperson = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.salesperson)

class Leaderboard(models.Model):
    salesperson = models.ForeignKey(to=Staff, on_delete=models.SET_NULL, null=True)
    points_today = models.DecimalField(max_digits=8, decimal_places=2)
    points_today = models.DecimalField(max_digits=8, decimal_places=2)
    points_today = models.DecimalField(max_digits=8, decimal_places=2)