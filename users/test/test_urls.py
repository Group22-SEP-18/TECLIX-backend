import pdb

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import RegisterStaffView, LoginWebStaffView, LoginSalespersonStaffView, GetLoggedUserFromToken, \
    GetDOAccountsView, UpdateSalespersonAccStateView, UpdateDistOfficerAccStateView
from knox import views as knox_views


class TestUrls(SimpleTestCase):

    def test_staff_register_url(self):
        url = reverse('staff:staff-register')
        self.assertEqual(resolve(url).func.view_class, RegisterStaffView)

    def test_web_login_url(self):
        url = reverse('staff:web-login')
        self.assertEqual(resolve(url).func.view_class, LoginWebStaffView)

    def test_mobile_login_url(self):
        url = reverse('staff:mobile-login')
        self.assertEqual(resolve(url).func.view_class, LoginSalespersonStaffView)

    def test_auto_login_url(self):
        url = reverse('staff:staff-logged-user')
        self.assertEqual(resolve(url).func.view_class, GetLoggedUserFromToken)

    def test_user_logout_url(self):
        url = reverse('staff:staff-logout')
        self.assertEqual(resolve(url).func.view_class, knox_views.LogoutView)

    def test_get_pending_do_account_url(self):
        url = reverse('staff:do-accounts')
        self.assertEqual(resolve(url).func.view_class, GetDOAccountsView)

    def test_approve_sp_account_url(self):
        url = reverse('staff:approve-sp', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, UpdateSalespersonAccStateView)

    def test_approve_do_account_url(self):
        url = reverse('staff:approve-do', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, UpdateDistOfficerAccStateView)
