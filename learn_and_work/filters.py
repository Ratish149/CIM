import django_filters
from .models import LearnAndWorkBooking


class LearnAndWorkBookingFilter(django_filters.FilterSet):
    zone = django_filters.CharFilter(field_name="zone", lookup_expr="icontains")
    date = django_filters.CharFilter(field_name="date", lookup_expr="icontains")
    school = django_filters.CharFilter(field_name="school", lookup_expr="icontains")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")

    class Meta:
        model = LearnAndWorkBooking
        fields = ["zone", "date", "school", "phone"]
