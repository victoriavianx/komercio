from django.test import TestCase
from django.core.exceptions import ValidationError

from faker import Faker

from products.models import Product
from accounts.models import Account

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.fake = Faker()

        seller_data = {
            "username": "victo",
            "first_name": "Victoria",
            "last_name": "Viana",
            "is_seller": True
        }

        cls.seller = Account.objects.create_user(**seller_data)

        seller_2_data = {
            "username": cls.fake.domain_word(),
            "first_name": cls.fake.first_name(),
            "last_name": cls.fake.last_name(),
            "is_seller": True
        }

        cls.seller_2 = Account.objects.create_user(**seller_2_data)

        product_data = {
            "description": cls.fake.sentence(nb_words=10, variable_nb_words=False),
            "price": cls.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "quantity": cls.fake.pyint(min_value=1, max_value=20),
            "is_active": cls.fake.pybool(),
            "seller": cls.seller
        }

        cls.products = [Product.objects.create(**product_data) for _ in range(5)]

    def test_product_cannot_belong_to_more_than_one_seller(self):
        print("test_product_cannot_belong_to_more_than_one_seller")

        for product in self.products:
            product.seller = self.seller_2
            product.save()
        
        for product in self.products:
            self.assertNotIn(product, self.seller.products.all())
            self.assertIn(product, self.seller_2.products.all())

    def test_product_fields(self):
        print("test_product_fields")

        product_data = {
            "description": self.fake.sentence(nb_words=10, variable_nb_words=False),
            "price": self.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            "quantity": self.fake.pyint(min_value=1, max_value=20),
            "is_active": self.fake.pybool(),
            "seller": self.seller
        }

        product = Product.objects.create(**product_data)

        self.assertEqual(product.description, product_data["description"])
        self.assertEqual(product.price, product_data["price"])
        self.assertEqual(product.quantity, product_data["quantity"])
        self.assertEqual(product.is_active, product_data["is_active"])
        self.assertEqual(product.seller, product_data["seller"])

    def test_wrong_type_fields(self):
        print("test_wrong_type_fields")

        with self.assertRaises(ValidationError):

            product_data = {
                "description": self.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                "price": self.fake.sentence(nb_words=10, variable_nb_words=False),
                "quantity": self.fake.pybool(),
                "is_active": self.fake.pyint(min_value=1, max_value=20),
                "seller": self.seller
            }

            Product.objects.create(**product_data)

