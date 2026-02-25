from rest_framework import serializers

from .models import GraduateRoster, Institute


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = "__all__"


class InstituteSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ["id", "institute_name", "institute_type", "logo"]


class GraduateRosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduateRoster
        fields = "__all__"
        extra_kwargs = {"institute": {"required": False}, "user": {"required": False}}


class GraduateRosterListSerializer(serializers.ModelSerializer):
    institute = InstituteSmallSerializer(read_only=True)

    class Meta:
        model = GraduateRoster
        fields = "__all__"
