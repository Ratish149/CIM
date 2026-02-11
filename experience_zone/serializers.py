from datetime import date

from rest_framework import serializers

from .models import ExperienceZoneBooking


class ExperienceZoneBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceZoneBooking
        fields = "__all__"
        read_only_fields = ["status", "created_at", "updated_at"]

    def validate_preferred_month(self, value):
        # Normalize to first day of the month
        normalized_date = value.replace(day=1)

        # Check if booking is for a past month
        today = date.today().replace(day=1)
        if normalized_date < today:
            raise serializers.ValidationError("Cannot book for a past month.")

        return normalized_date

    def validate(self, data):
        company_name = data.get("company_name")
        preferred_month = data.get("preferred_month")

        if company_name and preferred_month:
            # Check if this company already has a booking (Confirmed or Waitlisted) for this month
            exists = ExperienceZoneBooking.objects.filter(
                company_name__iexact=company_name,
                preferred_month=preferred_month.replace(day=1),
            ).exists()

            if exists:
                raise serializers.ValidationError(
                    {
                        "company_name": f"A booking for '{company_name}' already exists for this month."
                    }
                )

        return data

    def create(self, validated_data):
        preferred_month = validated_data.get("preferred_month")

        # Count confirmed bookings for this month
        confirmed_count = ExperienceZoneBooking.objects.filter(
            preferred_month=preferred_month, status="Confirmed"
        ).count()

        if confirmed_count < 50:
            validated_data["status"] = "Confirmed"
        else:
            validated_data["status"] = "Waitlisted"

        return super().create(validated_data)
