import json
from django.urls import reverse
from ..models import Staff
from customer_api.models import Customer, ServiceOrder
from salesperson_api.models import SalespersonLocation, Leaderboard
from .test_setup import TestSetUp

class TestView(TestSetUp):
    def approve_account(self, user_data):
        res1 = self.client.post(self.register_url, user_data, format='multipart')
        user = Staff.objects.get(email=res1.data['email'])
        user.is_approved = True
        user.save()
        return user

    def get_officer_header(self):
        officer = self.approve_account(user_data=self.register_officer_data)
        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        return header

    def get_manager_header(self):
        manager = self.approve_account(user_data=self.register_manager_data)
        login_res = self.client.post(self.web_login_url, self.login_cred_om)
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        return header

    def add_location(self):
        # create salesperson
        sp_register_result = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        sp = Staff.objects.get(email=sp_register_result.data['email'])
        sp.is_approved = True
        sp.save()

        # create new customer
        customer= Customer.objects.create(**self.customer_data)
        # create location
        location = SalespersonLocation.objects.create(customer=customer, salesperson=sp)
        return sp

    def add_serviceorder(self):
        # create salesperson
        sp_register_result = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        sp = Staff.objects.get(email=sp_register_result.data['email'])
        sp.is_approved = True
        sp.save()

        # create new customer
        customer= Customer.objects.create(**self.customer_data)
        # create serviceorder
        so = ServiceOrder.objects.create(customer=customer, salesperson=sp, original_price='0.00', discount='0.00')
        return sp

    def add_sp_to_leaderboard(self):
        # create salesperson
        sp_register_result = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        sp = Staff.objects.get(email=sp_register_result.data['email'])
        sp.is_approved = True
        sp.save()
        # add to leaderboard
        leaderboard = Leaderboard.objects.create(salesperson=sp, **self.leaderboard_data)
        return sp

    # SalespersonListView
    def test_do_can_get_salesperson_list(self):
        sp = self.approve_account(user_data=self.register_salesperson_data)
        header = self.get_officer_header()
        res = self.client.get(self.salespersons_base_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['email'], sp.email)

    def test_manager_can_get_salesperson_list(self):
        sp = self.approve_account(user_data=self.register_salesperson_data)
        header = self.get_manager_header()
        res = self.client.get(self.salespersons_base_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['email'], sp.email)

    # SalespersonView
    def test_do_can_get_single_salesperson(self):
        sp = self.approve_account(user_data=self.register_salesperson_data)
        header = self.get_officer_header()
        single_salesperson_url = reverse('salesperson:single-salesperson', kwargs={'id': sp.id})
        res = self.client.get(single_salesperson_url, **header, )
        self.assertEqual(res.data['email'], sp.email)

    def test_manager_can_get_single_salesperson(self):
        sp = self.approve_account(user_data=self.register_salesperson_data)
        header = self.get_manager_header()
        single_salesperson_url = reverse('salesperson:single-salesperson', kwargs={'id': sp.id})
        res = self.client.get(single_salesperson_url, **header, )
        self.assertEqual(res.data['email'], sp.email)

    # LocationListView
    def test_do_can_get_location_list(self):
        self.add_location()
        header = self.get_officer_header()
        res = self.client.get(self.locatation_list_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer']['latitude'], self.customer_data['latitude'])
        self.assertEqual(res.data[0]['customer']['longitude'], self.customer_data['longitude'])

    def test_manager_can_get_location_list(self):
        self.add_location()
        header = self.get_manager_header()
        res = self.client.get(self.locatation_list_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer']['latitude'], self.customer_data['latitude'])
        self.assertEqual(res.data[0]['customer']['longitude'], self.customer_data['longitude'])

    # CurrentLocationListView
    def test_do_can_get_current_location_list(self):
        self.add_location()
        header = self.get_officer_header()
        res = self.client.get(self.current_locatation_list_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer']['latitude'], self.customer_data['latitude'])
        self.assertEqual(res.data[0]['customer']['longitude'], self.customer_data['longitude'])

    def test_manager_can_get_current_location_list(self):
        self.add_location()
        header = self.get_manager_header()
        res = self.client.get(self.current_locatation_list_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer']['latitude'], self.customer_data['latitude'])
        self.assertEqual(res.data[0]['customer']['longitude'], self.customer_data['longitude'])

    # SalespersonLocationView
    def test_do_can_get_single_sp_location(self):
        sp = self.add_location()
        header = self.get_officer_header()
        locations_sp_url = reverse('salesperson:single-salesperson-locations', kwargs={'id': sp.id})
        res = self.client.get(locations_sp_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer']['latitude'], self.customer_data['latitude'])
        self.assertEqual(res.data[0]['customer']['longitude'], self.customer_data['longitude'])

    def test_manager_can_get_single_sp_location(self):
        sp = self.add_location()
        header = self.get_manager_header()
        locations_sp_url = reverse('salesperson:single-salesperson-locations', kwargs={'id': sp.id})
        res = self.client.get(locations_sp_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['customer']['latitude'], self.customer_data['latitude'])
        self.assertEqual(res.data[0]['customer']['longitude'], self.customer_data['longitude'])

    # SalespersonServiceOrdersView
    def test_do_can_get_single_sp_so(self):
        sp = self.add_serviceorder()
        header = self.get_officer_header()
        locations_sp_url = reverse('salesperson:all-salesperson-so', kwargs={'id': sp.id})
        res = self.client.get(locations_sp_url, **header, )
        self.assertEqual(len(res.data), 1)
        print(res.data)

    def test_manager_can_get_single_sp_so(self):
        sp = self.add_serviceorder()
        header = self.get_manager_header()
        locations_sp_url = reverse('salesperson:all-salesperson-so', kwargs={'id': sp.id})
        res = self.client.get(locations_sp_url, **header, )
        self.assertEqual(len(res.data), 1)

    # LeaderboardView
    def test_do_can_get_leaderboard_list(self):
        self.add_sp_to_leaderboard()
        header = self.get_officer_header()
        res = self.client.get(self.leaderboard_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['points_today'], self.leaderboard_data['points_today'])
        self.assertEqual(res.data[0]['points_current_month'], self.leaderboard_data['points_current_month'])
        self.assertEqual(res.data[0]['points_all_time'], self.leaderboard_data['points_all_time'])

    def test_manager_can_get_leaderboard_list(self):
        self.add_sp_to_leaderboard()
        header = self.get_manager_header()
        res = self.client.get(self.leaderboard_url, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['points_today'], self.leaderboard_data['points_today'])
        self.assertEqual(res.data[0]['points_current_month'], self.leaderboard_data['points_current_month'])
        self.assertEqual(res.data[0]['points_all_time'], self.leaderboard_data['points_all_time'])

    # LeaderboardPointSchemaView
    def test_manager_can_create_leaderboard_schema(self):
        header = self.get_manager_header()
        res = self.client.post(self.leaderboard_schema_url, self.leaderboard_schema_data, format='multipart', **header,)
        self.assertEqual(res.data['points_type'], self.leaderboard_schema_data['points_type'])
        self.assertEqual(res.data['percentage'], self.leaderboard_schema_data['percentage'])
        self.assertEqual(res.data['bonus_points'], self.leaderboard_schema_data['bonus_points'])
        self.assertEqual(res.status_code, 201)

    def test_do_can_not_create_leaderboard_schema(self):
        header = self.get_officer_header()
        res = self.client.post(self.leaderboard_schema_url, self.leaderboard_schema_data, format='multipart', **header,)
        self.assertEqual(res.status_code, 403)

    def test_manager_can_get_leaderboard_schema(self):
        header = self.get_manager_header()
        self.client.post(self.leaderboard_schema_url, self.leaderboard_schema_data, format='multipart', **header,)
        res = self.client.get(self.leaderboard_schema_url, **header,)
        self.assertEqual(res.data[0]['points_type'], self.leaderboard_schema_data['points_type'])
        self.assertEqual(res.data[0]['percentage'], self.leaderboard_schema_data['percentage'])
        self.assertEqual(res.data[0]['bonus_points'], self.leaderboard_schema_data['bonus_points'])
        self.assertEqual(res.status_code, 200)

    def test_do_can_not_get_leaderboard_schema(self):
        header = self.get_officer_header()
        manager_header = self.get_manager_header()
        self.client.post(self.leaderboard_schema_url, self.leaderboard_schema_data, format='multipart', **manager_header,)
        res = self.client.get(self.leaderboard_schema_url, **header,)
        self.assertEqual(res.status_code, 403)