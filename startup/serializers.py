from rest_framework import serializers

from startup.constants import TrackType
from startup.models import StartUpRegistration
from startup.services.email_service import send_registration_emails


class StartUpRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for BIC Pavilion enquiry registration.
    Maps and normalizes incoming HTML form inputs (e.g. s_name, b_biz, c_notes)
    to consolidated model fields (full_name, organization_name, notes).
    """

    class Meta:
        model = StartUpRegistration
        fields = "__all__"
        read_only_fields = ("id", "status", "created_at", "updated_at")

    def to_internal_value(self, data):
        """
        Flexibly accept both HTML form keys (s_name, b_biz, etc.)
        and canonical model field names (full_name, organization_name, etc.).
        """
        mutable_data = data.copy() if hasattr(data, "copy") else dict(data)

        # Normalize track input before ChoiceField validation runs
        if "track" in mutable_data:
            val = str(mutable_data["track"]).strip().lower()
            if val in ["school", "makerspace", "room 1", "room1"]:
                mutable_data["track"] = TrackType.MAKERSPACE
            elif val in ["college", "design studio", "design_studio", "room 2", "room2"]:
                mutable_data["track"] = TrackType.DESIGN_STUDIO
            elif val in ["business", "growth room", "growth_room", "room 3", "room3"]:
                mutable_data["track"] = TrackType.GROWTH_ROOM

        # Unified: Full Name
        if "full_name" not in mutable_data:
            mutable_data["full_name"] = (
                mutable_data.get("s_name")
                or mutable_data.get("c_name")
                or mutable_data.get("b_name")
                or ""
            )

        # Unified: Phone
        if "phone" not in mutable_data:
            mutable_data["phone"] = (
                mutable_data.get("s_phone")
                or mutable_data.get("c_phone")
                or mutable_data.get("b_phone")
                or ""
            )

        # Unified: Email
        if "email" not in mutable_data:
            mutable_data["email"] = (
                mutable_data.get("s_email")
                or mutable_data.get("c_email")
                or mutable_data.get("b_email")
                or None
            )

        # Unified: Organization / School / College / Business Name
        if "organization_name" not in mutable_data:
            mutable_data["organization_name"] = (
                mutable_data.get("s_school")
                or mutable_data.get("c_college")
                or mutable_data.get("b_biz")
                or mutable_data.get("school_name")
                or mutable_data.get("college_name")
                or mutable_data.get("business_name")
                or ""
            )

        # Unified: Role
        if "role" not in mutable_data:
            mutable_data["role"] = (
                mutable_data.get("s_role")
                or mutable_data.get("b_role")
                or mutable_data.get("school_role")
                or mutable_data.get("business_role")
                or ""
            )

        # Unified: Municipality / Location
        if "municipality" not in mutable_data:
            mutable_data["municipality"] = (
                mutable_data.get("s_place")
                or mutable_data.get("c_place")
                or mutable_data.get("b_place")
                or mutable_data.get("place")
                or ""
            )

        # Unified: Single Notes field for all
        if "notes" not in mutable_data:
            mutable_data["notes"] = (
                mutable_data.get("s_notes")
                or mutable_data.get("c_notes")
                or mutable_data.get("b_challenge")
                or ""
            )

        # Track 1: School (Makerspace) field mappings
        field_mappings = {
            "s_request": "school_request",
            "s_type": "school_type",
            "s_grades": "school_grades",
            "s_students": "school_students_count",
            "s_teachers": "school_teachers_count",
            "s_date1": "school_preferred_date_1",
            "s_date2": "school_preferred_date_2",
            "s_slot": "school_session_slot",
            "s_month": "school_session_month",
            "s_space": "school_available_space",
            # Track 2: College (Design Studio) mappings
            "c_gender": "gender",
            "c_age": "age_group",
            "c_prog": "college_programme",
            "c_year": "college_year",
            "c_stage": "idea_stage",
            "c_topics": "interested_topics",
            "c_channel": "preferred_contact_channel",
            "c_host": "willing_to_host_workshop",
            # Track 3: Business (Growth Room) mappings
            "b_district": "district",
            "b_reg": "business_registration_type",
            "b_years": "trading_duration",
            "b_sector": "business_sector",
            "b_staff": "employees_count",
            "b_turnover": "annual_turnover",
            "b_owner": "ownership_diversity",
            "b_interest": "area_of_interest",
            "b_day": "expo_visit_day",
            "b_needs": "support_needs",
            "b_challenge": "biggest_challenge",
            "heard": "heard_about_us",
            "updates": "keep_updated",
        }

        for old_key, new_key in field_mappings.items():
            if old_key in mutable_data and new_key not in mutable_data:
                mutable_data[new_key] = mutable_data[old_key]

        # Convert checkbox boolean representations
        if "willing_to_host_workshop" in mutable_data:
            val = mutable_data["willing_to_host_workshop"]
            if isinstance(val, str):
                mutable_data["willing_to_host_workshop"] = val.lower() in ["yes", "true", "1", "on"]

        if "consent" in mutable_data:
            val = mutable_data["consent"]
            if isinstance(val, str):
                mutable_data["consent"] = val.lower() in ["yes", "true", "1", "on"]

        if "keep_updated" in mutable_data:
            val = mutable_data["keep_updated"]
            if isinstance(val, str):
                mutable_data["keep_updated"] = val.lower() in ["yes", "true", "1", "on"]

        return super().to_internal_value(mutable_data)

    def validate(self, attrs: dict) -> dict:
        track = attrs.get("track")

        # Basic contact requirements for all tracks
        self._require(attrs, "full_name", "Full name is required.")
        self._require(attrs, "phone", "Mobile / phone number is required.")

        if track == TrackType.MAKERSPACE:
            self._require(attrs, "organization_name", "School name is required.")
            self._require(attrs, "school_request", "School request type is required.")
            self._require(attrs, "municipality", "Municipality / district is required.")
            self._require(attrs, "role", "Role / designation is required.")
            self._require_int_gt_zero(attrs, "school_students_count", "Number of students is required.")
            if not attrs.get("school_grades") or not str(attrs.get("school_grades")).strip():
                raise serializers.ValidationError({"school_grades": "Please select at least one grade."})

        elif track == TrackType.DESIGN_STUDIO:
            self._require(attrs, "organization_name", "College name is required.")
            self._require(attrs, "college_programme", "Faculty / programme is required.")
            self._require(attrs, "idea_stage", "Idea stage is required.")
            self._require(attrs, "preferred_contact_channel", "Preferred contact channel is required.")

        elif track == TrackType.GROWTH_ROOM:
            self._require(attrs, "organization_name", "Business name is required.")
            self._require(attrs, "role", "Role in business is required.")
            self._require(attrs, "district", "District is required.")
            self._require(attrs, "business_registration_type", "Registration type is required.")
            self._require(attrs, "trading_duration", "Time trading is required.")
            self._require(attrs, "business_sector", "Business sector is required.")
            self._require(attrs, "area_of_interest", "Area of interest is required.")

        if not attrs.get("consent"):
            raise serializers.ValidationError({"consent": "Consent is required to submit this enquiry."})

        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        send_registration_emails(instance)
        return instance

    @staticmethod
    def _require(attrs: dict, field: str, message: str) -> None:
        value = attrs.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            raise serializers.ValidationError({field: message})

    @staticmethod
    def _require_int_gt_zero(attrs: dict, field: str, message: str) -> None:
        value = attrs.get(field)
        if not value or value < 1:
            raise serializers.ValidationError({field: message})


class StartUpRegistrationListSerializer(serializers.ModelSerializer):
    """
    Lightweight read-only serializer for list views.
    """

    class Meta:
        model = StartUpRegistration
        fields = (
            "id",
            "track",
            "status",
            "full_name",
            "phone",
            "email",
            "organization_name",
            "role",
            "municipality",
            "heard_about_us",
            "consent",
            "keep_updated",
            "created_at",
        )
