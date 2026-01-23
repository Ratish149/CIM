import django_filters
from django.db.models import Q
from django.utils import timezone

from .models import Event


class EventFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(
        method="filter_is_active", label="Is Active (Upcoming/Ongoing)"
    )

    class Meta:
        model = Event
        fields = ["status", "is_featured", "is_popular"]

    def filter_is_active(self, queryset, name, value):
        if value:
            # Events that are NOT over (end_date >= today OR end_date is NULL)
            return queryset.filter(
                Q(end_date__gte=timezone.now().date()) | Q(end_date__isnull=True)
            )
        return queryset
