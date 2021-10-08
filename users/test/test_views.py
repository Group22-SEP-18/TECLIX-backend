import pdb

from .test_setup import TestSetUp
from ..models import Staff


class TestView(TestSetUp):
    def approve_account(self, user_data):
        res1 = self.client.post(self.register_url, user_data, format='multipart')
        # approving account
        user_email = email = res1.data['email']
        user = Staff.objects.get(email=user_email)
        user.is_approved = True
        user.save()

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
        self.register_salesperson_data['first_name'] = 'name@'
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        # pdb.set_trace()
        self.assertEqual(res.data['non_field_errors'][0], 'The first name should only contain letters')
        self.assertEqual(res.status_code, 400)

    # login view
    def test_user_cannot_login_without_data(self):
        res = self.client.post(self.mobile_login_url)
        self.assertEqual(res.status_code, 400)

    def test_mobile_user_cannot_login_without_being_approved(self):
        user = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        res = self.client.post(self.mobile_login_url, self.login_cred)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'Your account is not approved.')
        self.assertEqual(res.status_code, 401)

    def test_web_user_cannot_login_without_being_approved(self):
        user = self.client.post(self.register_url, self.register_officer_data, format='multipart')
        res = self.client.post(self.mobile_login_url, self.login_cred)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'Your account is not approved.')
        self.assertEqual(res.status_code, 401)

    def test_mobile_user_can_login(self):
        self.approve_account(user_data=self.register_salesperson_data)
        res = self.client.post(self.mobile_login_url, self.login_cred)
        # pdb.set_trace()

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_web_user_can_login(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.web_login_url, self.login_cred)
        # pdb.set_trace()

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_web_user_can_not_login_to_mobile_app(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.mobile_login_url, self.login_cred)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'You are not authorized to use the application.')
        self.assertEqual(res.status_code, 401)

    def test_mobile_user_can_not_login_to_web_app(self):
        self.approve_account(user_data=self.register_salesperson_data)
        res = self.client.post(self.web_login_url, self.login_cred)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'You are not authorized to use the application.')
        self.assertEqual(res.status_code, 401)

    def test_mobile_user_auto_login_via_token(self):
        self.approve_account(user_data=self.register_salesperson_data)
        res = self.client.post(self.mobile_login_url, self.login_cred)

        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.get(self.logged_user, **header)

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_web_user_auto_login_via_token(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.web_login_url, self.login_cred)

        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.get(self.logged_user, **header)

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_user_can_not_auto_login_once_logged_out(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.web_login_url, self.login_cred)

        res = self.client.get(self.logged_user)

        # pdb.set_trace()
        self.assertEqual(res.data['detail'], 'Authentication credentials were not provided.')

        self.assertEqual(res.status_code, 401)

    def test__user_can_not_auto_with_invalid_token(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.web_login_url, self.login_cred)

        token = 'dummy-token'
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.get(self.logged_user, **header)

        # pdb.set_trace()
        self.assertEqual(res.data['detail'], 'Invalid token.')

        self.assertEqual(res.status_code, 401)
