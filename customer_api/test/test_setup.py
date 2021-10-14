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
        self.get_all_so = reverse('customer:all-so')
        self.create_so = reverse('customer:create-so')

        # quires

        LeaderboardPointSchema.objects.create(points_type='CUSTOMER_CREATION', bonus_points=0.0, percentage=10)
        Product.objects.create(short_name=self.faker.first_name(), long_name=self.faker.first_name(), barcode='test123',
                               category="cookies", price='20.00')

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
        self.login_cred = {
            "email": 'test1@gmail.com',
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

        self.so_data = {
            "order_items": [],
            "so_type": "later",
            "original_price": "1250",
            "discount": "100.00",
            "customer": 1
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
