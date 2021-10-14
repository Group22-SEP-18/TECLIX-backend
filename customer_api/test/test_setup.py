from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
import io
from salesperson_api.models import LeaderboardPointSchema
from asset_api.models import Product
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
        self.faker = Faker()

        # urls
        self.customer_base_url = reverse('customer:all-customers')
        self.sp_register = reverse('staff:staff-register')
        self.sp_login = reverse('staff:mobile-login')
        self.web_login = reverse('staff:web-login')
        self.get_all_so = reverse('customer:all-so')
        self.create_so = reverse('customer:create-so')
        self.get_all_lp = reverse('customer:all-late-pay')
        self.create_lp = reverse('customer:add-late-pay')
        self.create_loyalty_points = reverse('customer:create-loyalty-points')

        # quires

        LeaderboardPointSchema.objects.create(points_type='CUSTOMER_CREATION', bonus_points=0.0, percentage=10)
        LeaderboardPointSchema.objects.create(points_type='LATE_PAYMENTS', bonus_points=0.0, percentage=10)

        # salesperson data data
        self.salesperson_data = {
            "email": 'test1@gmail.com',
            "employee_no": 'testid1',
            "password": 'password',
            "user_role": 'SALESPERSON',
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "contact_no": '1234567890',
            "profile_picture": generate_photo_file(),
        }
        self.manager_data = {
            "email": 'test3@gmail.com',
            "employee_no": 'testid2',
            "password": 'password',
            "user_role": 'MANAGER',
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

        self.customer_data = {
            "shop_name": self.faker.first_name(),
            "owner_first_name": self.faker.first_name(),
            "owner_last_name": self.faker.last_name(),
            "email": "cus1@gmail.com",
            "contact_no": "0123456789",
            "latitude": "1.000",
            "longitude": "2.000",
            "street": self.faker.city(),
            "city": self.faker.city(),
            "district": "Matale",
            "loyalty_points": "0.00",
            "outstanding": "0.00",
        }

        self.loyalty_data = {
            "minimum_amount": "100.00",
            "max_amount": "200.00",
            "point_percentage": 15
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
