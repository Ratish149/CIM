from rest_framework import serializers

from .models import (
    CustomUser,
    File,
    Organization,
)
from .services.user_service import change_user_password_by_email


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ("id", "organization", "name", "file", "uploaded_at")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            "bio",
            "date_of_birth",
            "phone_number",
            "address",
            "designation",
            "alternate_no",
            "avatar",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserSerializerForJobSeeker(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "bio",
            "date_of_birth",
            "phone_number",
            "address",
            "designation",
            "alternate_no",
            "avatar",
        )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "address",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data.get("email")
        email = validated_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        user = CustomUser.objects.create_user(**validated_data, username=username)
        return user


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "avatar")


class OrganizationSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = (
            "id",
            "user",
            "name",
            "email",
            "phone_number",
            "address",
            "country",
            "province_state",
            "municipality_ward",
            "website",
            "logo",
            "files",
        )


class ChangePasswordByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def to_internal_value(self, data):
        if isinstance(data, dict) and "password" in data and "new_password" not in data:
            data = data.copy()
            data["new_password"] = data["password"]
        return super().to_internal_value(data)

    def validate_email(self, value):
        email = value.strip()
        if not CustomUser.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return email

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )
        return value

    def save(self, **kwargs):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        return change_user_password_by_email(email=email, new_password=new_password)
