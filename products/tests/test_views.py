from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status, Response

from django.core.exceptions import ValidationError

from faker import Faker

from accounts.models import Account
from products.models import Product

class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/products/"

        cls.fake = Faker()

        seller_data = {
            "username": "victo",
            "password": "1234",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        seller_2_data = {
            "username": "naruto",
            "password": "1234",
            "first_name": "Naruto",
            "last_name": "Uzumaki",
            "is_seller": True
        }

        not_seller_data = {
            "username": "alex",
            "password": "abcd",
            "first_name": "Alexandre",
            "last_name": "Alves",
            "is_seller": False
        }

        cls.wrong_data = {}

        cls.seller = Account.objects.create_user(**seller_data)
        cls.seller_token = Token.objects.create(user=cls.seller)

        seller_2 = Account.objects.create_user(**seller_2_data)
        cls.seller_2_token = Token.objects.create(user=seller_2)

        common_user = Account.objects.create_user(**not_seller_data)
        cls.common_user_token = Token.objects.create(user=common_user)

        cls.product_data = {
            "description": cls.fake.sentence(nb_words=10, variable_nb_words=False),
            "price": cls.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "quantity": cls.fake.pyint(min_value=1, max_value=20),
            "is_active": cls.fake.pybool(),
            "seller": cls.seller
        }

        [Product.objects.create(**cls.product_data) for _ in range(5)]

    def test_only_a_seller_user_can_add_product(self):
        print("test_only_a_seller_user_can_add_product")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response_seller = self.client.post(self.base_url, data=self.product_data)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response_seller.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_common_user_cannot_add_product(self):
        print("test_common_user_cannot_add_product")
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.common_user_token.key)
        response_not_seller = self.client.post(self.base_url, data=self.product_data)

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response_not_seller.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_return_response_of_registered_product(self):
        print("test_return_response_of_registered_product")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response_seller = self.client.post(self.base_url, data=self.product_data)
        data = response_seller.json()

        required_fields = ["id", "description", "price", "quantity", "is_active", "seller"]

        for field in required_fields:
            self.assertIn(field, data.keys())

    def test_retrieve_all_products(self):
        print("test_retrieve_all_products")

        response = self.client.get(self.base_url)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_specific_return_for_retrieve_of_products(self):
        print("test_specific_return_for_retrieve_of_products")

        response = self.client.get(self.base_url)
        data = response.json()

        required_fields = ["id", "description", "price", "quantity", "is_active", "seller"]

        for field in required_fields:
            self.assertIn(field, data["results"][0].keys())

    def test_missing_fields(self):
        print("test_missing_fields")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)    
        response = self.client.post(self.base_url, data=self.wrong_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_quantity_cannot_be_negative(self):
        print("test_quantity_cannot_be_negative")

        product = {
            "description": self.fake.sentence(nb_words=10, variable_nb_words=False),
            "price": self.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "quantity": -5,
            "is_active": self.fake.pybool(),
            "seller": self.seller
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)    
        response = self.client.post(self.base_url, data=product)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

##########################################
class ProductDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = Faker()

        seller_data = {
            "username": "victo",
            "password": "1234",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        seller_2_data = {
            "username": "naruto",
            "password": "1234",
            "first_name": "Naruto",
            "last_name": "Uzumaki",
            "is_seller": True
        }

        seller = Account.objects.create_user(**seller_data)
        cls.seller_token = Token.objects.create(user=seller)

        seller_2 = Account.objects.create_user(**seller_2_data)
        cls.seller_2_token = Token.objects.create(user=seller_2)

        cls.product_data = {
            "description": cls.fake.sentence(nb_words=10, variable_nb_words=False),
            "price": cls.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "quantity": cls.fake.pyint(min_value=1, max_value=20),
            "is_active": cls.fake.pybool(),
            "seller": seller
        }

        product = Product.objects.create(**cls.product_data)

        cls.base_url_detail = f"/api/products/{product.id}/"

    def test_seller_user_can_update_own_product(self):
        print("test_seller_user_can_update_own_product")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response = self.client.patch(self.base_url_detail, data={"description": "nome_produto"})

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
    
    def test_seller_cannot_update_product_from_another_seller(self):
        print("test_seller_cannot_update_product_from_another_seller")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_2_token.key)
        response = self.client.patch(self.base_url_detail, data={"description": "nome_produto"})

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_retrieve_a_specific_product(self):
        print("test_retrieve_a_specific_product")

        response = self.client.get(self.base_url_detail)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)