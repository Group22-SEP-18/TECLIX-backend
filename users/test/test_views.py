import pdb

from .test_setup import TestSetUp
from ..models import Staff
from django.urls import reverse


class TestStaffView(TestSetUp):
    def approve_account(self, user_data):
        res1 = self.client.post(self.register_url, user_data, format='multipart')
        # approving account
        # pdb.set_trace()
        user = Staff.objects.get(email=res1.data['email'])
        # pdb.set_trace()
        user.is_approved = True
        user.save()
        return user

    # register view related
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

    def test_user_contact_should_contain_only_digits(self):
        self.register_salesperson_data['contact_no'] = 'numbe111'
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        # pdb.set_trace()
        self.assertEqual(res.data['non_field_errors'][0], 'the contact number should only contain numbers.')
        self.assertEqual(res.status_code, 400)

    def test_user_first_name_should_contain_only_letters(self):
        self.register_salesperson_data['first_name'] = 'name@'
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        # pdb.set_trace()
        self.assertEqual(res.data['non_field_errors'][0], 'The first name should only contain letters')
        self.assertEqual(res.status_code, 400)

    def test_user_last_name_should_contain_only_letters(self):
        self.register_salesperson_data['last_name'] = 'name@'
        res = self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        # pdb.set_trace()
        self.assertEqual(res.data['non_field_errors'][0], 'The last name should only contain letters')
        self.assertEqual(res.status_code, 400)

    # login view
    def test_user_cannot_login_without_data(self):
        res = self.client.post(self.mobile_login_url)
        self.assertEqual(res.status_code, 400)

    def test_mobile_user_cannot_login_without_being_approved(self):
        self.client.post(self.register_url, self.register_salesperson_data, format='multipart')
        res = self.client.post(self.mobile_login_url, self.login_cred_sp)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'Your account is not approved.')
        self.assertEqual(res.status_code, 401)

    def test_web_user_cannot_login_without_being_approved(self):
        self.client.post(self.register_url, self.register_officer_data, format='multipart')
        res = self.client.post(self.web_login_url, self.login_cred_do)

        self.assertEqual(res.data['detail'], 'Your account is not approved.')
        self.assertEqual(res.status_code, 401)

    def test_mobile_user_can_login(self):
        self.approve_account(user_data=self.register_salesperson_data)
        res = self.client.post(self.mobile_login_url, self.login_cred_sp)
        # pdb.set_trace()

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_web_user_can_login(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.web_login_url, self.login_cred_om)
        # pdb.set_trace()

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_mobile_user_can_not_login_with_invalid_credentials(self):
        self.approve_account(user_data=self.register_salesperson_data)
        self.login_cred_sp['password'] = 'wrong_pw'
        res = self.client.post(self.mobile_login_url, self.login_cred_sp)

        self.assertEqual(res.data['detail'], 'Invalid credentials')
        self.assertEqual(res.status_code, 401)

    def test_web_user_can_not_login_with_invalid_credentials(self):
        self.approve_account(user_data=self.register_manager_data)
        self.login_cred_om['password'] = 'wrong_pw'
        res = self.client.post(self.web_login_url, self.login_cred_om)

        self.assertEqual(res.data['detail'], 'Invalid credentials')
        self.assertEqual(res.status_code, 401)

    # def test_mobile_user_can_not_login_when_account_is_disabled(self):
    #     user = self.approve_account(user_data=self.register_salesperson_data)
    #     user.is_active = False
    #     user.save()
    #     res = self.client.post(self.mobile_login_url, self.login_cred_sp)
    #     pdb.set_trace()
    #
    #     self.assertEqual(res.data['detail'], 'Your account is disabled.')
    #     self.assertEqual(res.status_code, 401)

    def test_web_user_can_not_login_to_mobile_app(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.mobile_login_url, self.login_cred_om)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'You are not authorized to use the application.')
        self.assertEqual(res.status_code, 401)

    def test_mobile_user_can_not_login_to_web_app(self):
        self.approve_account(user_data=self.register_salesperson_data)
        res = self.client.post(self.web_login_url, self.login_cred_sp)
        # pdb.set_trace()

        self.assertEqual(res.data['detail'], 'You are not authorized to use the application.')
        self.assertEqual(res.status_code, 401)

    def test_mobile_user_auto_login_via_token(self):
        self.approve_account(user_data=self.register_salesperson_data)
        res = self.client.post(self.mobile_login_url, self.login_cred_sp)

        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.get(self.logged_user, **header)

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_web_user_auto_login_via_token(self):
        self.approve_account(user_data=self.register_manager_data)
        res = self.client.post(self.web_login_url, self.login_cred_om)

        token = res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.get(self.logged_user, **header)

        self.assertIsNotNone(res.data['token'])
        self.assertEqual(res.status_code, 200)

    def test_user_can_not_auto_login_once_logged_out(self):
        self.approve_account(user_data=self.register_manager_data)
        self.client.post(self.web_login_url, self.login_cred_om)

        res = self.client.get(self.logged_user)

        # pdb.set_trace()
        self.assertEqual(res.data['detail'], 'Authentication credentials were not provided.')

        self.assertEqual(res.status_code, 401)

    def test_user_can_not_auto_with_invalid_token(self):
        self.approve_account(user_data=self.register_manager_data)
        self.client.post(self.web_login_url, self.login_cred_om)

        token = 'dummy-token'
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.get(self.logged_user, **header)

        # pdb.set_trace()
        self.assertEqual(res.data['detail'], 'Invalid token.')

        self.assertEqual(res.status_code, 401)

    def test_officer_can_approve_salesperson_acc(self):
        sp = self.approve_account(user_data=self.register_salesperson_data)

        self.approve_account(user_data=self.register_officer_data)

        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        approve_sp = reverse('staff:approve-sp', kwargs={'id': sp.id})
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.post(approve_sp, {'is_approved': True}, **header, )

        # pdb.set_trace()
        self.assertTrue(res.data['is_approved'])

        self.assertEqual(res.status_code, 201)

    def test_officer_can_reject_salesperson_acc(self):
        sp = self.approve_account(user_data=self.register_salesperson_data)

        self.approve_account(user_data=self.register_officer_data)

        login_res = self.client.post(self.web_login_url, self.login_cred_do)
        approve_sp = reverse('staff:approve-sp', kwargs={'id': sp.id})
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.post(approve_sp, {'is_approved': False}, **header, )

        # pdb.set_trace()
        self.assertFalse(res.data['is_approved'])

        self.assertEqual(res.status_code, 201)

    def test_manager_can_approve_officer_acc(self):
        officer = self.approve_account(user_data=self.register_officer_data)

        self.approve_account(user_data=self.register_manager_data)

        login_res = self.client.post(self.web_login_url, self.login_cred_om)
        approve_sp = reverse('staff:approve-do', kwargs={'id': officer.id})
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.post(approve_sp, {'is_approved': True}, **header, )

        # pdb.set_trace()
        self.assertTrue(res.data['is_approved'])

        self.assertEqual(res.status_code, 201)

    def test_manager_can_reject_officer_acc(self):
        res1 = self.client.post(self.register_url, self.register_officer_data, format='multipart')
        officer = Staff.objects.get(email=res1.data['email'])

        manager = self.approve_account(user_data=self.register_manager_data)

        login_res = self.client.post(self.web_login_url, self.login_cred_om)
        approve_do = reverse('staff:approve-do', kwargs={'id': officer.id})
        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}
        res = self.client.post(approve_do, {'is_approved': False}, **header, )

        self.assertFalse(res.data['is_approved'])
        self.assertFalse(officer.is_rejected)
        self.assertEqual(res.status_code, 201)

    def test_get_pending_DO_accounts(self):
        officer = self.approve_account(user_data=self.register_officer_data)
        manager = self.approve_account(user_data=self.register_manager_data)

        login_res = self.client.post(self.web_login_url, self.login_cred_om)

        token = login_res.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token ' + token}

        res = self.client.get(self.pending_do, **header, )
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['email'], officer.email)
