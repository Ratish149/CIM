from rest_framework import serializers

from .models import IncubationCenter, RescheduleRequest


class IncubationCenterSerializer(serializers.ModelSerializer):
    has_pending_reschedule_request = serializers.SerializerMethodField()

    class Meta:
        model = IncubationCenter
        fields = "__all__"

    def get_has_pending_reschedule_request(self, obj):
        return obj.reschedule_requests.filter(status="Pending").exists()


class RescheduleRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RescheduleRequest
        fields = "__all__"
