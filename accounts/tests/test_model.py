from django.test import TestCase
from django.db.utils import IntegrityError

from accounts.models import Account

class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
       
        cls.user_1_data = {
            "username": "victo",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        cls.user_1 = Account.objects.create_user(**cls.user_1_data)

    def test_username_cannot_be_repeated(self):
        print("test_username_cannot_be_repeated")
        
        with self.assertRaises(IntegrityError):
            user_2_data = {
                "username": "victo",
                "first_name": "Toria",
                "last_name": "Viana",
                "is_seller": False
            }

            Account.objects.create_user(**user_2_data)

    def test_firstname_and_lastname_max_length(self):
        print("test_firstname_and_lastname_max_length")

        user = Account.objects.get(username="victo")
        name_max_length = user._meta.get_field("first_name").max_length
        lastname_max_length = user._meta.get_field("last_name").max_length

        self.assertEqual(name_max_length, 50)
        self.assertEqual(lastname_max_length, 50)

    def test_type_is_seller_field(self):
        print("test_type_is_seller_field")

        self.assertIs(type(self.user_1_data["is_seller"]), bool)