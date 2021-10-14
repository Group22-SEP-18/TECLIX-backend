import pdb

from .test_setup import TestSetUp
from users.models import Staff
from customer_api.models import Customer, ServiceOrder
from django.urls import reverse
from salesperson_api.models import Leaderboard


class TestCustomerView(TestSetUp):

    def generate_request_header(self):
        res1 = self.client.post(self.sp_register, self.salesperson_data, format='multipart')
        user = Staff.objects.get(email=res1.data['email'])
        user.is_approved = True
        user.save()
        Leaderboard.objects.create(salesperson=user)

        #     login
        res = self.client.post(self.sp_login, self.login_cred)
        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        return header

    def return_customer_obj(self):
        Customer.objects.create(**self.customer_data)
        customer = Customer.objects.get(email=self.customer_data['email'])
        return customer

    def test_create_customer_account(self):
        header = self.generate_request_header()
        res = self.client.post(self.customer_base_url, self.customer_data, **header)
        self.assertEqual(res.data['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 201)

    def test_get_all_customer_accounts(self):
        header = self.generate_request_header()
        Customer.objects.create(**self.customer_data)
        res = self.client.get(self.customer_base_url, **header)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data[0]['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 200)

    def test_get_customer(self):
        header = self.generate_request_header()
        customer = self.return_customer_obj()

        self.get_customer_url = reverse('customer:single-customer', kwargs={'id': customer.id})

        res = self.client.get(self.get_customer_url, **header)

        self.assertEqual(res.data['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 200)

    def test_return_customer_search_results(self):
        header = self.generate_request_header()
        customer = self.return_customer_obj()
        self.search_customer = reverse('customer:search-customer')
        res = self.client.get(self.search_customer + '?search=' + customer.shop_name, **header)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.status_code, 200)

    def test_return_empty_search_results(self):
        header = self.generate_request_header()

        self.search_customer = reverse('customer:search-customer')
        res = self.client.get(self.search_customer + '?search=' + 'test', **header)
        self.assertEqual(len(res.data), 0)
        self.assertEqual(res.status_code, 200)

    def test_get_all_so(self):
        header = self.generate_request_header()

        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()

        ServiceOrder.objects.create(customer=customer, salesperson=sp, original_price='0.00', discount='0.00')

        res = self.client.get(self.get_all_so, **header)
        self.assertEqual(res.data[0]['customer']['shop_name'], customer.shop_name)
        self.assertEqual(res.data[0]['order_items'], [])
        self.assertEqual(res.status_code, 200)

    # def test_create_so(self):
    #     header = self.generate_request_header()
    #     self.client.post(self.customer_base_url, self.customer_data, **header)
    # 
    #     res = self.client.post(self.create_so, self.so_data, **header)
    #     pdb.set_trace()

    def test_get_so_given_id(self):
        header = self.generate_request_header()

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
        header = self.generate_request_header()

        sp = Staff.objects.get(email='test1@gmail.com')
        customer = self.return_customer_obj()
        ServiceOrder.objects.create(customer=customer, salesperson=sp, original_price='0.00', discount='0.00')

        self.get_so_cus = reverse('customer:all-customer-so', kwargs={'id': customer.id})

        res = self.client.get(self.get_so_cus, **header)
        self.assertEqual(res.data[0]['customer']['shop_name'], customer.shop_name)
        self.assertEqual(res.data[0]['order_items'], [])
        self.assertEqual(res.status_code, 200)
