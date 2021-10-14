import datetime
import json
import pdb

from .test_setup import TestSetUp
from users.models import Staff
from customer_api.models import Customer, ServiceOrder, CustomerLatePay, CustomerLoyaltyPointScheme
from asset_api.models import Product, VehicleSalesperson, Vehicle, VehicleProduct
from django.urls import reverse
from salesperson_api.models import Leaderboard


class TestCustomerView(TestSetUp):

    def generate_sp_request_header(self):
        res1 = self.client.post(self.sp_register, self.salesperson_data, format='multipart')
        user = Staff.objects.get(email=res1.data['email'])
        user.is_approved = True
        user.save()
        Leaderboard.objects.create(salesperson=user)

        #     login
        res = self.client.post(self.sp_login, self.login_cred_sp)
        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        return header

    def create_so_related_objs(self):
        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()
        product = Product.objects.create(short_name=self.faker.first_name(), long_name=self.faker.first_name(),
                                         barcode='test123',
                                         category="cookies", price='20.00')
        self.vehicle_data['created_by'] = sp
        vehicle = Vehicle.objects.create(**self.vehicle_data)
        vsp = VehicleSalesperson.objects.create(vehicle=vehicle, salesperson=sp, assigned_by=sp)
        VehicleProduct.objects.create(vehicle_salesperson=vsp, product=product, quantity=10)

        return [product, customer, sp]

    def generate_manager_request_header(self):
        res1 = self.client.post(self.sp_register, self.manager_data, format='multipart')
        user = Staff.objects.get(email=res1.data['email'])
        user.is_approved = True
        user.save()

        res = self.client.post(self.web_login, self.login_cred_om)
        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        return header

    def return_customer_obj(self):
        Customer.objects.create(**self.customer_data)
        customer = Customer.objects.get(email=self.customer_data['email'])
        return customer

    def test_create_customer_account(self):
        header = self.generate_sp_request_header()
        res = self.client.post(self.customer_base_url, self.customer_data, **header)
        self.assertEqual(res.data['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 201)

    def test_get_all_customer_accounts(self):
        header = self.generate_sp_request_header()
        Customer.objects.create(**self.customer_data)
        res = self.client.get(self.customer_base_url, **header)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data[0]['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 200)

    def test_get_customer(self):
        header = self.generate_sp_request_header()
        customer = self.return_customer_obj()

        self.get_customer_url = reverse('customer:single-customer', kwargs={'id': customer.id})

        res = self.client.get(self.get_customer_url, **header)

        self.assertEqual(res.data['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 200)

    def test_return_customer_search_results(self):
        header = self.generate_sp_request_header()
        customer = self.return_customer_obj()
        self.search_customer = reverse('customer:search-customer')
        res = self.client.get(self.search_customer + '?search=' + customer.shop_name, **header)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.status_code, 200)

    def test_return_empty_search_results(self):
        header = self.generate_sp_request_header()

        self.search_customer = reverse('customer:search-customer')
        res = self.client.get(self.search_customer + '?search=' + 'test', **header)
        self.assertEqual(len(res.data), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_all_so(self):
        header = self.generate_sp_request_header()

        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()

        ServiceOrder.objects.create(customer=customer, salesperson=sp, original_price='0.00', discount='0.00')

        res = self.client.get(self.get_all_so, **header)
        self.assertEqual(res.data[0]['customer']['shop_name'], customer.shop_name)
        self.assertEqual(res.data[0]['order_items'], [])
        self.assertEqual(res.status_code, 200)

    def test_create_so_now(self):
        header = self.generate_sp_request_header()
        product, customer, sp = self.create_so_related_objs()

        self.so_data = {
            "order_items": [
                {
                    "quantity": 5,
                    "price_at_the_time": "120.00",
                    "product": product.id
                },
            ],
            "so_type": "later",
            "original_price": "1250.00",
            "discount": "100.00",
            "customer": customer.id
        }

        res = self.client.post(self.create_so, json.dumps(self.so_data), **header, content_type='application/json')
        self.assertEqual(res.data['customer'], customer.id)
        self.assertEqual(res.data['original_price'], self.so_data['original_price'])
        self.assertEqual(res.status_code, 201)

    def test_create_so_later(self):
        header = self.generate_sp_request_header()
        product, customer, sp = self.create_so_related_objs()
        self.so_data = {
            "order_items": [
                {
                    "quantity": 5,
                    "price_at_the_time": "120.00",
                    "product": product.id
                },
            ],
            "so_type": "now",
            "original_price": "1250.00",
            "discount": "100.00",
            "customer": customer.id
        }

        res = self.client.post(self.create_so, json.dumps(self.so_data), **header, content_type='application/json')
        self.assertEqual(res.data['customer'], customer.id)
        self.assertEqual(res.data['original_price'], self.so_data['original_price'])
        self.assertEqual(res.status_code, 201)

    def test_create_so_will_reject_products_with_quantity_more_than_actual_stocks(self):
        header = self.generate_sp_request_header()
        product, customer, sp = self.create_so_related_objs()
        self.so_data = {
            "order_items": [
                {
                    "quantity": 12,
                    "price_at_the_time": "120.00",
                    "product": product.id
                },
            ],
            "so_type": "now",
            "original_price": "1250.00",
            "discount": "100.00",
            "customer": customer.id
        }
        res = self.client.post(self.create_so, json.dumps(self.so_data), **header, content_type='application/json')
        self.assertEqual(res.data[0], 'Quantity requested is not in stocks.')
        self.assertEqual(res.status_code, 400)

    def test_get_so_given_id(self):
        header = self.generate_sp_request_header()

        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()
        ServiceOrder.objects.create(customer=customer, salesperson=sp, original_price='0.00', discount='0.00')
        so = ServiceOrder.objects.get(customer=customer)
        self.get_so = reverse('customer:get-so', kwargs={'id': so.id})

        res = self.client.get(self.get_so, **header)
        self.assertEqual(res.data['customer']['shop_name'], customer.shop_name)
        self.assertEqual(res.data['order_items'], [])
        self.assertEqual(res.status_code, 200)

    def test_get_all_so_given_customer(self):
        header = self.generate_sp_request_header()

        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()
        ServiceOrder.objects.create(customer=customer, salesperson=sp, original_price='0.00', discount='0.00')

        self.get_so_cus = reverse('customer:all-customer-so', kwargs={'id': customer.id})

        res = self.client.get(self.get_so_cus, **header)
        self.assertEqual(res.data[0]['customer']['shop_name'], customer.shop_name)
        self.assertEqual(res.data[0]['order_items'], [])
        self.assertEqual(res.status_code, 200)

    def test_get_all_late_payments(self):
        header = self.generate_sp_request_header()
        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()

        CustomerLatePay.objects.create(customer=customer, salesperson=sp, amount="0.00")
        res = self.client.get(self.get_all_lp, **header)
        # pdb.set_trace()

        self.assertEqual(res.data[0]['customer']['shop_name'], customer.shop_name)
        self.assertEqual(res.data[0]['date'], datetime.date.today().isoformat())
        self.assertEqual(res.status_code, 200)

    def test_create_late_pay(self):
        header = self.generate_sp_request_header()
        customer = self.return_customer_obj()

        res = self.client.post(self.create_lp, {'customer': customer, 'amount': '100.00'}, **header)
        self.assertEqual(res.data['customer'], customer.id)
        self.assertEqual(res.data['date'], datetime.date.today().isoformat())
        self.assertEqual(res.status_code, 201)

    def test_get_all_late_pay_given_customer(self):
        header = self.generate_sp_request_header()
        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()

        CustomerLatePay.objects.create(customer=customer, salesperson=sp, amount="0.00")

        self.get_lp_per_cus = reverse('customer:per-customer-late-pay', kwargs={'id': customer.id})
        res = self.client.get(self.get_lp_per_cus, **header)

        self.assertEqual(res.data[0]['salesperson']['employee_no'], sp.employee_no)
        self.assertEqual(res.data[0]['customer'], customer.id)
        self.assertEqual(res.data[0]['date'], datetime.date.today().isoformat())
        self.assertEqual(res.status_code, 200)

    def test_create_loyalty_point_option(self):
        header = self.generate_manager_request_header()

        res = self.client.post(self.create_loyalty_points, self.loyalty_data, **header)

        self.assertEqual(res.data['minimum_amount'], self.loyalty_data['minimum_amount'])
        self.assertEqual(res.status_code, 201)

    def test_delete_loyalty_point_option(self):
        header = self.generate_manager_request_header()
        schema = CustomerLoyaltyPointScheme.objects.create(**self.loyalty_data)
        self.delete_loyalty = reverse('customer:delete-loyalty-points', kwargs={'pk': schema.id})
        res = self.client.delete(self.delete_loyalty, **header)

        self.assertEqual(res.status_code, 204)
