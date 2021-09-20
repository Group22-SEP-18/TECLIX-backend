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
    points_today = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    points_current_month = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    points_all_time = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)


class LeaderboardPointSchema(models.Model):
    POINTS_TYPE_OPTIONS = {
        ('LATE_PAYMENTS', 'Late Payments'),
        ('SO', 'Service Orders'),
        ('ITEM_COUNT', 'Item Count')
    }
    points_type = models.CharField(choices=POINTS_TYPE_OPTIONS, max_length=100)
    price_lowerbound = models.DecimalField(max_digits=11, decimal_places=2)
    price_upperbound = models.DecimalField(max_digits=11, decimal_places=2)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    bonus_points = models.DecimalField(max_digits=8, decimal_places=2)
