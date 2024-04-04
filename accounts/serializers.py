from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "username", "first_name", "last_name",
            "email", "phone", "password", "is_active",
            "photo", "bio", "is_staff", "date_joined",
        )
        read_only_fields = ("id", "is_staff", "is_active", "date_joined",)
        extra_kwargs = {
            "password": {
                "validators": [validate_password],
                "required": True,
                "write_only": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "username": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "email": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "phone": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if not password:
            raise ValidationError("Please provide password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
