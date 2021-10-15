import pdb

from .test_setup import TestSetUp
from ..models import Staff
from django.urls import reverse


class TestView(TestSetUp):
    def approve_account(self, user_data):
        res1 = self.client.post(self.register_url, user_data, format='multipart')
        # approving account
        # pdb.set_trace()
        user = Staff.objects.get(email=res1.data['email'])
        # pdb.set_trace()
        user.is_approved = True
        user.save()
        return user

    # def vehicle_products_salesperson(self, products_id, salesperson_id, quantity, vehicle_id):
    #     assign_products_salesperson = {
    #         "assigned_vehicle": [
    #                                 {
    #                                     "quantity": quantity,
    #                                     "product": products_id
    #                                 }
    #                             ],
    #         "vehicle": vehicle_id,
    #         "salesperson": salesperson_id
    #     }
    #     return(assign_products_salesperson)

    def test_do_can_register_products(self):
        self.approve_account(user_data=self.register_officer_data)
        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.post(self.register_product_url, self.register_product_data, **header, format='multipart')
        self.assertEqual(res.data['barcode'], self.register_product_data['barcode'])

    def test_do_can_register_vehicles(self):
        self.approve_account(user_data=self.register_officer_data)
        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.post(self.register_vehicle_url, self.register_vehicle_data, **header, format='multipart')
        self.assertEqual(res.data['vehicle_number'], self.register_vehicle_data['vehicle_number'])

    def test_get_all_vehicles(self):
        officer = self.approve_account(user_data=self.register_officer_data)
        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        self.client.post(self.register_vehicle_url, self.register_vehicle_data, **header, format='multipart')
        res = self.client.get(self.get_all_vehicles, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['vehicle_number'], self.register_vehicle_data['vehicle_number'])

    def test_assign_to_vehicle(self):
        officer = self.approve_account(user_data=self.register_officer_data)
        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}

        product = self.client.post(self.register_product_url, self.register_product_data, **header, format='multipart')
        vehicle = self.client.post(self.register_vehicle_url, self.register_vehicle_data, **header, format='multipart')
        salesperson = self.approve_account(user_data=self.register_salesperson_data)

        # assignments = self.vehicle_products_salesperson(vehicle_id = vehicle.data['id'],products_id = product.data['id'], salesperson_id = salesperson.id, quantity = 3)
        print(product.data['id'])
        print(vehicle.data['id'])
        print(salesperson.id)
        print(self.assign_products_salesperson)
        res = self.client.post(self.assign_vehicle, self.assign_products_salesperson, **header, )
        pdb.set_trace()
        # print(res.data)



    
    # def test_get_all_assigned_vehicles(self):
        


