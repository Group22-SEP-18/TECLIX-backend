from ..models import Staff
from django.test import TestCase, RequestFactory
from ..permissions import IsOfficer, IsManager, IsSalesperson
from ..views import UpdateSalespersonAccStateView


class TestUserPermissions(TestCase):
    def setUp(self):
        self.salesperson = Staff.objects.create_user(email='test@gmail.com', employee_no='Emp111',
                                                     user_role='SALESPERSON',
                                                     first_name='test', last_name='test', contact_no='1478523690',
                                                     profile_picture='testImg.png')
        self.manager = Staff.objects.create_user(email='test2@gmail.com', employee_no='Emp1112',
                                                 user_role='MANAGER',
                                                 first_name='test', last_name='test', contact_no='1478523690',
                                                 profile_picture='testImg.png')
        self.officer = Staff.objects.create_user(email='test3@gmail.com', employee_no='Emp1113',
                                                 user_role='OFFICER',
                                                 first_name='test', last_name='test', contact_no='1478523690',
                                                 profile_picture='testImg.png')
        self.factory = RequestFactory()

    def test_check_salesperson_permission(self):
        request = self.factory.delete('/')
        request.user = self.salesperson

        permission_check = IsSalesperson()
        permission = permission_check.has_permission(request, None)
        permission_obj = permission_check.has_object_permission(request, None, None)
        self.assertTrue(permission)
        self.assertTrue(permission_obj)

    def test_check_officer_permission(self):
        request = self.factory.delete('/')
        request.user = self.officer

        permission_check = IsOfficer()
        permission = permission_check.has_permission(request, None)
        permission_obj = permission_check.has_object_permission(request, None, None)
        self.assertTrue(permission)
        self.assertTrue(permission_obj)

    def test_check_manager_permission(self):
        request = self.factory.delete('/')
        request.user = self.manager

        permission_check = IsManager()
        permission = permission_check.has_permission(request, None)
        permission_obj = permission_check.has_object_permission(request, None, None)
        self.assertTrue(permission)
        self.assertTrue(permission_obj)

    def tearDown(self):
        return super().tearDown()
