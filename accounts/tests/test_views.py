from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from accounts.models import Account

class AccountRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/accounts/"
        cls.seller_data = {
            "username": "victo",
            "password": "1234",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        cls.common_user = {
            "username": "alex",
            "password": "abcd",
            "first_name": "Alexandre",
            "last_name": "Alves",
            "is_seller": False
        }

        cls.wrong_data = {}

    def test_can_register_seller_account(self):
        print("test_can_register_seller_account")

        response = self.client.post(self.base_url, data=self.seller_data)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

        
    def test_can_register_common_account(self):
        print("test_can_register_common_account")

        response = self.client.post(self.base_url, data=self.common_user)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_account_fields(self):
        print("test_account_fields")

        response = self.client.post(self.base_url, data=self.seller_data)

        expected_return_fields = ("id", "username", "first_name", "last_name", "is_seller", "date_joined", "is_active", "is_superuser")

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_missing_fields(self):
        print("test_missing_fields")

        response = self.client.post(self.base_url, data=self.wrong_data)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

        required_fields = ["username", "password", "first_name", "last_name"]

        for field in required_fields:
            self.assertIn(field, response.data.keys())


class LoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url = "/api/login/"

        seller_data = {
            "username": "victo",
            "password": "1234",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        not_seller_data = {
            "username": "alex",
            "password": "abcd",
            "first_name": "Alexandre",
            "last_name": "Alves",
            "is_seller": False
        }

        Account.objects.create_user(**seller_data)

        Account.objects.create_user(**not_seller_data)

        cls.seller_credentials = {
            "username": "victo",
            "password": "1234"
        }

        cls.not_seller_credentials = {
            "username": "alex",
            "password": "abcd"
        }

    def test_return_token_field(self):
        print("test_return_token_field")

        response_seller = self.client.post(self.base_url, data=self.seller_credentials)
        response_not_seller = self.client.post(self.base_url, data=self.not_seller_credentials)

        self.assertIn("token", response_seller.data)
        self.assertIn("token", response_not_seller.data)


class AccountAuthTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client: APIClient        
        
        seller_data = {
            "username": "victo",
            "password": "1234",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        not_seller_data = {
            "username": "alex",
            "password": "abcd",
            "first_name": "Alexandre",
            "last_name": "Alves",
            "is_seller": False
        }

        admin_data = {
            "username": "rosi",
            "password": "123456",
            "first_name": "Rosi",
            "last_name": "Naldo",
            "is_seller": False
        }

        seller = Account.objects.create_user(**seller_data)
        cls.seller_token = Token.objects.create(user=seller)

        common_user = Account.objects.create_user(**not_seller_data)
        cls.common_user_token = Token.objects.create(user=common_user)

        admin = Account.objects.create_superuser(**admin_data)
        cls.admin_token = Token.objects.create(user=admin)

        cls.base_url = "/api/accounts/"
        cls.base_url_detail = f"/api/accounts/{seller.id}/"
        cls.base_url_management = f"/api/accounts/{common_user.id}/management/"

    def test_user_can_update_own_account(self):
        print("test_user_can_update_own_account")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.seller_token.key)
        response = self.client.patch(self.base_url_detail, data={"first_name": "Ipsaluna"})

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
    
    def test_user_cannot_update_account_from_another_user(self):
        print("test_user_cannot_update_account_from_another_user")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.common_user_token.key)
        response = self.client.patch(self.base_url_detail, data={"first_name": "Ipsaluna"})

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_just_admin_can_update_is_active_field(self):
        print("test_just_admin_can_update_is_active_field")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.admin_token.key)
        response = self.client.patch(self.base_url_management, data={"is_active": False})

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_can_retrieve_all_users(self):
        print("test_can_retrieve_all_users")

        response = self.client.get(self.base_url)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)