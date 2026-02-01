from rest_framework import serializers

from .models import (
    CustomUser,
    File,
    Organization,
)


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
