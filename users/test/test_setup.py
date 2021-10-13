from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
import io

from PIL import Image


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


class TestSetUp(APITestCase):
    def setUp(self):
        self.register_url = reverse('staff:staff-register')
        self.mobile_login_url = reverse('staff:mobile-login')
        self.web_login_url = reverse('staff:web-login')
        self.logged_user = reverse('staff:staff-logged-user')
        self.pending_do = reverse('staff:do-accounts')

        self.faker = Faker()

        # login data
        self.register_salesperson_data = {
            "email": 'test1@gmail.com',
            "employee_no": 'testid1',
            "password": 'password',
            "user_role": 'SALESPERSON',
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "contact_no": '1234567890',
            "profile_picture": generate_photo_file(),
        }
        self.register_manager_data = {
            "email": 'test3@gmail.com',
            "employee_no": 'testid2',
            "password": 'password',
            "user_role": 'MANAGER',
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "contact_no": '1234567890',
            "profile_picture": generate_photo_file(),
        }
        self.register_officer_data = {
            "email": 'test2@gmail.com',
            "employee_no": 'testid3',
            "password": 'password',
            "user_role": 'OFFICER',
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "contact_no": '1234567890',
            "profile_picture": generate_photo_file(),
        }

        self.login_cred_sp = {
            "email": 'test1@gmail.com',
            "password": 'password',

        }
        self.login_cred_om = {
            "email": 'test3@gmail.com',
            "password": 'password',

        }
        self.login_cred_do = {
            "email": 'test2@gmail.com',
            "password": 'password',

        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
