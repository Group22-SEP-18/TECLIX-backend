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
        self.web_login_url = reverse('staff:web-login')
        self.sp_login = reverse('staff:mobile-login')
        self.customer_base_url = reverse('customer:all-customers')
        self.salespersons_base_url = reverse('salesperson:all-salespersons')
        self.create_so_url = reverse('customer:create-so')
        self.locatation_list_url = reverse('salesperson:all-locations')
        self.current_locatation_list_url = reverse('salesperson:all-current-locations')
        self.leaderboard_url = reverse('salesperson:leaderboard')
        self.leaderboard_schema_url = reverse('salesperson:leaderboard-point-schema')
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

        self.customer_data = {
            "shop_name": self.faker.first_name(),
            "owner_first_name": self.faker.first_name(),
            "owner_last_name": self.faker.last_name(),
            "email": "cus1@gmail.com",
            "contact_no": "0123456789",
            "latitude": "6.98430639", 
            "longitude": "79.93313804",
            "street": self.faker.city(),
            "city": self.faker.city(),
            "district": "Matale",
            "loyalty_points": "0.00",
            "outstanding": "0.00",
        }

        self.leaderboard_data = {
            "points_today": "10.00",
            "points_current_month": "100.00",
            "points_all_time": "1000.00",
        }

        self.leaderboard_schema_data = {
            "points_type": "LATE_PAYMENTS",
            "percentage": "10.00",
            "bonus_points": "1000.00",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
