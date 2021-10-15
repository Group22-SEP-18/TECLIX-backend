import pdb

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ProductListView, ProductView, VehicleCreateView, VehicleView, VehicleListView, \
    AssignVehicleItemsView, AssignedProductsListVehicleView, AllAssignedProductsListVehicleView


class TestUrls(SimpleTestCase):

    def test_all_products_url(self):
        url = reverse('asset:all-products')
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_single_product_url(self):
        url = reverse('asset:single-product', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, ProductView)

    def test_all_vehicles_url(self):
        url = reverse('asset:all-vehicles')
        self.assertEqual(resolve(url).func.view_class, VehicleListView)

    def test_create_vehicle_url(self):
        url = reverse('asset:create-vehicle')
        self.assertEqual(resolve(url).func.view_class, VehicleCreateView)

    def test_single_vehicle_url(self):
        url = reverse('asset:single-vehicle', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, VehicleView)

    def test_assign_vehicle_items_url(self):
        url = reverse('asset:assign-vehicle-items')
        self.assertEqual(resolve(url).func.view_class, AssignVehicleItemsView)

    def test_get_vehicle_items_url(self):
        url = reverse('asset:get-vehicle-items')
        self.assertEqual(resolve(url).func.view_class, AssignedProductsListVehicleView)

    def test_all_vehicle_items_url(self):
        url = reverse('asset:all-vehicle-items')
        self.assertEqual(resolve(url).func.view_class, AllAssignedProductsListVehicleView)
