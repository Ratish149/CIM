from rest_framework import serializers

from .models import (
    GuidedTour,
    Invitation,
    Panelist,
    SponsorBooking,
    StallBooking,
    SubSession,
    ThematicRegistration,
    ThematicSession,
)


class StallBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StallBooking
        fields = "__all__"


class StallBookingSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = StallBooking
        fields = ["company", "stall_no", "status"]


class SponsorBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorBooking
        fields = "__all__"


class PanelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panelist
        fields = ["role", "name", "profile_image", "company", "location", "biodata"]


class SubSessionSerializer(serializers.ModelSerializer):
    panelists = PanelistSerializer(many=True, read_only=True)

    class Meta:
        model = SubSession
        fields = ["id", "title", "description", "panelists"]


class ThematicSessionSerializer(serializers.ModelSerializer):
    thematicpanelists = PanelistSerializer(many=True, read_only=True)
    sub_sessions = SubSessionSerializer(many=True, read_only=True)

    class Meta:
        model = ThematicSession
        fields = [
            "id",
            "title",
            "date",
            "start_time",
            "end_time",
            "thematicpanelists",
            "description",
            "sub_sessions",
        ]


class ThematicRegistrationSerializer(serializers.ModelSerializer):
    sessions = ThematicSessionSerializer(many=True, read_only=True)

    class Meta:
        model = ThematicRegistration
        fields = [
            "id",
            "name",
            "organization",
            "designation",
            "address",
            "email",
            "contact",
            "opportunity_theme1",
            "opportunity_theme2",
            "opportunity_theme3",
            "business_connections",
            "participant",
            "arrival_date",
            "departure_date",
            "flight_no",
            "flight_time",
            "return_flight_no",
            "return_flight_time",
            "airline",
            "food",
            "hotel_accomodation",
            "check_in_date",
            "check_out_date",
            "hotel",
            "status",
            "sessions",
            "additional_info",
            "presentation_slide",
            "opportunity_wall",
        ]


class GuidedTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidedTour
        fields = "__all__"


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"
