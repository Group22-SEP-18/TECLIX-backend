from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import SalespersonListView, SalespersonView, LocationListView, \
    CurrentLocationListView, SalespersonLocationView, SalespersonServiceOrdersView, \
    LeaderboardView, LeaderboardPointSchemaView


class TestUrls(SimpleTestCase):

    def test_get_all_salespersons(self):
        url = reverse('salesperson:all-salespersons')
        self.assertEqual(resolve(url).func.view_class, SalespersonListView)

    def test_get_single_salesperson(self):
        url = reverse('salesperson:single-salesperson', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, SalespersonView)

    def test_get_all_locations(self):
        url = reverse('salesperson:all-locations')
        self.assertEqual(resolve(url).func.view_class, LocationListView)

    def test_get_all_current_locations_for_salespersons(self):
        url = reverse('salesperson:all-current-locations')
        self.assertEqual(resolve(url).func.view_class, CurrentLocationListView)

    def test_get_all_locations_single_salesperson(self):
        url = reverse('salesperson:single-salesperson-locations', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, SalespersonLocationView)

    def test_get_all_serviceorders_single_salesperson(self):
        url = reverse('salesperson:all-salesperson-so', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, SalespersonServiceOrdersView)

    def test_get_leaderboard(self):
        url = reverse('salesperson:leaderboard')
        self.assertEqual(resolve(url).func.view_class, LeaderboardView)

    def test_get_leaderboard_point_schema(self):
        url = reverse('salesperson:leaderboard-point-schema')
        self.assertEqual(resolve(url).func.view_class, LeaderboardPointSchemaView)
