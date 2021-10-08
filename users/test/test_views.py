import pdb

from .test_setup import TestSetUp
from ..models import Staff


class TestView(TestSetUp):
    # resgister view related
    def test_user_cannot_register_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_salesperson_can_register(self):
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        self.assertEqual(res.data['email'], self.register_salesperson_data['email'])
        self.assertEqual(res.data['user_role'], 'SALESPERSON')
        self.assertEqual(res.status_code, 201)

    def test_user_manager_can_register(self):
        res = self.client.post(self.register_url, self.register_manager_data, format='multipart')
        self.assertEqual(res.data['email'], self.register_manager_data['email'])
        self.assertEqual(res.data['user_role'], 'MANAGER')

        self.assertEqual(res.status_code, 201)

    def test_user_officer_can_register(self):
        res = self.client.post(self.register_url, self.register_officer_data, format='multipart')
        self.assertEqual(res.data['email'], self.register_officer_data['email'])
        self.assertEqual(res.data['user_role'], 'OFFICER')

        self.assertEqual(res.status_code, 201)

    def test_user_contact_should_contain_ten_digits(self):
        self.register_salesperson_data['contact_no'] = '123456'
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        # pdb.set_trace()
        self.assertEqual(res.data['non_field_errors'][0], 'the contact number must be 10 digits long.')
        self.assertEqual(res.status_code, 400)

    def test_user_first_name_should_contain_only_letters(self):
        self.register_salesperson_data['first_name'] = 'bin2'
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        # pdb.set_trace()
        self.assertEqual(res.data['non_field_errors'][0], 'The first name should only contain letters')
        self.assertEqual(res.status_code, 400)

#
