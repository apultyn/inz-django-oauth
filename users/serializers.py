from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import NewUser


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = NewUser
        fields = ("email", "password", "confirm_password")

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "The two password fields didn’t match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)

        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["groups"] = list(user.groups.values_list("name", flat=True))

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME

        data["expires_in"] = int(access_token_lifetime.total_seconds())
        return data
