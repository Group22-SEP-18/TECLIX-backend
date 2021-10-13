from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import CustomerListView, CustomerView, SearchCustomerView, ServiceOrderListView, CreateServiceOrderView, \
    ServiceOrderView, CustomerServiceOrdersView, AllCustomerLatePayView, CreateLatePayView, CustomerLatePayView, \
    CreateLoyaltyPointsView, DeleteLoyaltyPointsView


class TestUrls(SimpleTestCase):

    def test_get_all_customer(self):
        url = reverse('customer:all-customers')
        self.assertEqual(resolve(url).func.view_class, CustomerListView)

    def test_get_single_customer(self):
        url = reverse('customer:single-customer', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, CustomerView)

    def test_search_customers(self):
        url = reverse('customer:search-customer')
        self.assertEqual(resolve(url).func.view_class, SearchCustomerView)

    def test_get_all_service_orders(self):
        url = reverse('customer:all-so')
        self.assertEqual(resolve(url).func.view_class, ServiceOrderListView)

    def test_create_service_order(self):
        url = reverse('customer:create-so')
        self.assertEqual(resolve(url).func.view_class, CreateServiceOrderView)

    def test_get_single_service_order(self):
        url = reverse('customer:get-so', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, ServiceOrderView)

    def test_get_all_service_orders_given_customer(self):
        url = reverse('customer:all-customer-so', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, CustomerServiceOrdersView)

    def test_get_all_late_payments(self):
        url = reverse('customer:all-late-pay')
        self.assertEqual(resolve(url).func.view_class, AllCustomerLatePayView)

    def test_create_late_payment(self):
        url = reverse('customer:add-late-pay')
        self.assertEqual(resolve(url).func.view_class, CreateLatePayView)

    def test_get_customer_late_payment(self):
        url = reverse('customer:per-customer-late-pay', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, CustomerLatePayView)

    def test_register_loyalty_point_option(self):
        url = reverse('customer:create-loyalty-points')
        self.assertEqual(resolve(url).func.view_class, CreateLoyaltyPointsView)

    def test_delete_loyalty_point_option(self):
        url = reverse('customer:delete-loyalty-points', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, DeleteLoyaltyPointsView)
