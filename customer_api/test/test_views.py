import pdb

from .test_setup import TestSetUp
from ..models import Staff
from django.urls import reverse
from salesperson_api.models import Leaderboard


class TestView(TestSetUp):

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

    def test_create_customer_account(self):
        header = self.generate_request_header()
        res = self.client.post(self.customer_base_url, self.customer_data, **header)
        self.assertEqual(res.data['shop_name'], self.customer_data['shop_name'])
        self.assertEqual(res.data['email'], self.customer_data['email'])
        self.assertEqual(res.status_code, 201)
