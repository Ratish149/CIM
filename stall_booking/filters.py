import django_filters
from django.db.models import Q

from .models import ThematicRegistration


class ThematicRegistrationFilter(django_filters.FilterSet):
    """
    FilterSet for ThematicRegistration allowing searching and filtering
    by name, contact number, and organization.
    """

    search = django_filters.CharFilter(
        method="filter_by_search",
        label="Search (name, contact number, organization)",
    )
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Name",
    )
    number = django_filters.CharFilter(
        field_name="contact",
        lookup_expr="icontains",
        label="Contact Number",
    )
    contact = django_filters.CharFilter(
        field_name="contact",
        lookup_expr="icontains",
        label="Contact Number",
    )
    organization = django_filters.CharFilter(
        field_name="organization",
        lookup_expr="icontains",
        label="Organization",
    )
    participant = django_filters.ChoiceFilter(
        field_name="participant",
        choices=ThematicRegistration.PARTICIPANT_TYPE_CHOICES,
        label="Participant Type",
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=ThematicRegistration.STATUS_CHOICES,
        label="Status",
    )

    class Meta:
        model = ThematicRegistration
        fields = [
            "search",
            "name",
            "number",
            "contact",
            "organization",
            "participant",
            "status",
        ]

    def filter_by_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(contact__icontains=value)
            | Q(organization__icontains=value)
        )
