from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import LearnAndWorkBookingFilter
from .models import LearnAndWorkBooking
from .serializers import LearnAndWorkBookingSerializer
from .utils import send_learn_and_work_emails


class LearnAndWorkBookingListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/learn-and-work/bookings/         — List all bookings (admin use)
    POST /api/learn-and-work/bookings/         — Submit a new booking request

    GET supports filtering via django-filter (zone, date, school, phone).
    POST is public — no authentication required.
    """
    queryset = LearnAndWorkBooking.objects.all()
    serializer_class = LearnAndWorkBookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LearnAndWorkBookingFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_learn_and_work_emails(serializer.instance)
        return Response(
            {
                "detail": "Booking request received. CIM will confirm by phone or email.",
                "id": serializer.instance.id,
                "zone": serializer.instance.zone,
                "date": serializer.instance.date,
                "time": serializer.instance.time,
                "school": serializer.instance.school,
            },
            status=status.HTTP_201_CREATED,
        )


class LearnAndWorkBookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/learn-and-work/bookings/<id>/  — Retrieve a booking
    PUT    /api/learn-and-work/bookings/<id>/  — Full update
    PATCH  /api/learn-and-work/bookings/<id>/  — Partial update
    DELETE /api/learn-and-work/bookings/<id>/  — Delete a booking
    """
    queryset = LearnAndWorkBooking.objects.all()
    serializer_class = LearnAndWorkBookingSerializer
