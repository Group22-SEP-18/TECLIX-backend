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
        self.register_product_url = reverse('asset:all-products')
        self.register_vehicle_url = reverse('asset:create-vehicle')
        self.get_all_vehicles = reverse('asset:all-vehicles')
        self.assign_vehicle = reverse('asset:assign-vehicle-items')
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
        #product data
        self.register_product_data = {
            "short_name": 'short name',
            "long_name": 'long name',
            "barcode": 'A-000010-Z',
            "category": 'biscuit',
            "price": 120,
            "product_image": generate_photo_file(),
        }
        #vehicle data
        self.register_vehicle_data = {
            "vehicle_number": 'WB-1234',
            "vehicle_type": 'THREEWHEELER',
            "vehicle_model": 'Piaggio',
            "vehicle_image": generate_photo_file(),
        }
        #vehicle products salesperson assignment
        self.assign_products_salesperson = {
            "assigned_vehicle": [
                                    {
                                        "quantity": 3,
                                        "product": 1
                                    }
                                ],
            "vehicle": 1,
            "salesperson": 2
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
