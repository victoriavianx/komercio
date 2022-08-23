from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=Account.objects.all(), message=["username already exists"])]
    )

    class Meta:
        model = Account
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser"
        ]
        read_only_fields = ["date_joined", "is_active", "is_superuser"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> Account:
        user_account = Account.objects.create_user(**validated_data)

        return user_account

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
