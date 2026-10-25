import django_filters
from django.db.models import Q

from .models import JobApplication, WorkInterest


class JobApplicationFilter(django_filters.FilterSet):
    job = django_filters.CharFilter(
        field_name="job__slug",
        lookup_expr="exact",
    )
    slug = django_filters.CharFilter(
        field_name="job__slug",
        lookup_expr="exact",
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=JobApplication.STATUS_CHOICES,
    )

    class Meta:
        model = JobApplication
        fields = ["status", "job", "slug"]


class WorkInterestFilterSet(django_filters.FilterSet):
    unit_group = django_filters.NumberFilter(
        field_name="unit_group__id", lookup_expr="exact"
    )
    proficiency_level = django_filters.CharFilter(
        field_name="proficiency_level", lookup_expr="exact"
    )
    availability = django_filters.CharFilter(
        field_name="availability", lookup_expr="exact"
    )
    skills = django_filters.CharFilter(method="filter_skills")

    class Meta:
        model = WorkInterest
        fields = []

    def filter_skills(self, queryset, name, value):
        if not value:
            return queryset
        skill_names = [s.strip() for s in value.split(",") if s.strip()]
        if not skill_names:
            return queryset

        query = Q()
        for skill_name in skill_names:
            query |= Q(skills__name__icontains=skill_name)

        return queryset.filter(query).distinct()
