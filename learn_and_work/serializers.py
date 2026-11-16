from rest_framework import serializers

from .models import LearnAndWorkBooking


class LearnAndWorkBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnAndWorkBooking
        fields = "__all__"
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        required = {
            "zone": "Zone is required.",
            "date": "Date is required.",
            "time": "Session time is required.",
            "school": "School or group name is required.",
            "grade": "Class or grade is required.",
            "teacher": "Teacher or contact person name is required.",
            "phone": "Mobile number is required.",
            "students": "Number of students is required.",
        }
        errors = {}
        for field, msg in required.items():
            if not str(attrs.get(field, "")).strip():
                errors[field] = msg
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
