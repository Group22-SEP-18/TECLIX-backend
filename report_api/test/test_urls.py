from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import GetMonthlySalespersonSalesView, GetSalespersonMonthlySales, GetDailyStatsView, GetMonthlyComparison


class TestUrls(SimpleTestCase):

    def test_get_monthly_salesperson_sales_stats(self):
        url = reverse('report:salesperson-month', kwargs={'sp': 1})
        self.assertEqual(resolve(url).func.view_class, GetMonthlySalespersonSalesView)

    def test_get_monthly_salesperson_total_sales(self):
        url = reverse('report:salesperson-all-month', kwargs={'sp': 1})
        self.assertEqual(resolve(url).func.view_class, GetSalespersonMonthlySales)

    def test_get_salesperson_daily_stats(self):
        url = reverse('report:salesperson-daily', kwargs={'sp': 1})
        self.assertEqual(resolve(url).func.view_class, GetDailyStatsView)

    def test_get_salesperson_monthly_stats_comparison(self):
        url = reverse('report:salesperson-monthly-comp', kwargs={'sp': 1})
        self.assertEqual(resolve(url).func.view_class, GetMonthlyComparison)
