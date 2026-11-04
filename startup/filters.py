import django_filters
from startup.models import StartUpRegistration


class StartUpRegistrationFilter(django_filters.FilterSet):
    track = django_filters.CharFilter(field_name="track", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    heard_about_us = django_filters.CharFilter(field_name="heard_about_us", lookup_expr="iexact")
    consent = django_filters.BooleanFilter(field_name="consent")
    keep_updated = django_filters.BooleanFilter(field_name="keep_updated")
    created_at_from = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at_to = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    # Consolidated contact & location
    full_name = django_filters.CharFilter(field_name="full_name", lookup_expr="icontains")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    organization_name = django_filters.CharFilter(field_name="organization_name", lookup_expr="icontains")
    municipality = django_filters.CharFilter(field_name="municipality", lookup_expr="icontains")

    # School-specific
    school_request = django_filters.CharFilter(field_name="school_request", lookup_expr="iexact")
    school_type = django_filters.CharFilter(field_name="school_type", lookup_expr="iexact")

    # College-specific
    college_programme = django_filters.CharFilter(field_name="college_programme", lookup_expr="icontains")
    idea_stage = django_filters.CharFilter(field_name="idea_stage", lookup_expr="iexact")
    willing_to_host_workshop = django_filters.BooleanFilter(field_name="willing_to_host_workshop")

    # Business-specific
    district = django_filters.CharFilter(field_name="district", lookup_expr="iexact")
    business_sector = django_filters.CharFilter(field_name="business_sector", lookup_expr="iexact")
    business_registration_type = django_filters.CharFilter(field_name="business_registration_type", lookup_expr="iexact")
    area_of_interest = django_filters.CharFilter(field_name="area_of_interest", lookup_expr="iexact")
    trading_duration = django_filters.CharFilter(field_name="trading_duration", lookup_expr="iexact")

    class Meta:
        model = StartUpRegistration
        fields = [
            "track", "status", "heard_about_us", "consent", "keep_updated",
            "created_at_from", "created_at_to",
            "full_name", "phone", "email", "organization_name", "municipality",
            "school_request", "school_type",
            "college_programme", "idea_stage", "willing_to_host_workshop",
            "district", "business_sector", "business_registration_type", "area_of_interest", "trading_duration",
        ]
