from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.validators import UniqueValidator

class Account(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name"]
