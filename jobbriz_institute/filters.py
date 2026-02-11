import django_filters

from .models import GraduateRoster


class GraduateRosterFilter(django_filters.FilterSet):
    trade_stream = django_filters.CharFilter(
        field_name="subject_trade_stream", lookup_expr="icontains", label="Trade/Stream"
    )
    level = django_filters.ChoiceFilter(
        field_name="level_completed",
        choices=GraduateRoster.LEVEL_COMPLETED_CHOICES,
        label="Level",
    )
    passed_year_min = django_filters.NumberFilter(
        field_name="passed_year", lookup_expr="gte", label="Passed Year (Min)"
    )
    passed_year_max = django_filters.NumberFilter(
        field_name="passed_year", lookup_expr="lte", label="Passed Year (Max)"
    )
    district = django_filters.CharFilter(
        field_name="current_district", lookup_expr="icontains", label="District"
    )
    municipality = django_filters.CharFilter(
        field_name="current_municipality", lookup_expr="icontains", label="Municipality"
    )
    status = django_filters.ChoiceFilter(
        field_name="job_status",
        choices=GraduateRoster.JOB_STATUS_CHOICES,
        label="Status",
    )
    certifying_agency = django_filters.ChoiceFilter(
        field_name="certifying_agency",
        choices=GraduateRoster.CERTIFYING_AGENCY_CHOICES,
        label="Certifying Agency",
    )
    institution_name = django_filters.CharFilter(
        field_name="institute__institute_name",
        lookup_expr="icontains",
        label="Institution Name",
    )

    class Meta:
        model = GraduateRoster
        fields = [
            "trade_stream",
            "level",
            "passed_year_min",
            "passed_year_max",
            "district",
            "municipality",
            "status",
            "certifying_agency",
            "institution_name",
        ]
