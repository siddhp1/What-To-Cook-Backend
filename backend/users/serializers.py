from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from zxcvbn import zxcvbn
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        if "password" in data and "confirm_password" in data:
            if data["password"] != data["confirm_password"]:
                raise serializers.ValidationError("Passwords do not match.")

            # Password strength check using zxcvbn
            password = data["password"]
            result = zxcvbn(password)
            if result.get("score") < 3:
                raise serializers.ValidationError("Password is not strong enough.")

        # Check if the email is unique
        if "email" in data:
            email = data["email"]
            user = self.instance
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise serializers.ValidationError("Email is already in use.")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        data["email"] = self.user.email
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name

        return data
