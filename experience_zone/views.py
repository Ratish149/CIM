from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExperienceZoneBooking
from .serializers import ExperienceZoneBookingSerializer


class ExperienceZoneBookingCreateView(generics.ListCreateAPIView):
    serializer_class = ExperienceZoneBookingSerializer

    def get_queryset(self):
        queryset = ExperienceZoneBooking.objects.all().order_by("-created_at")

        month = self.request.query_params.get("month")
        year = self.request.query_params.get("year")

        if year:
            queryset = queryset.filter(preferred_month__year=year)
        if month:
            queryset = queryset.filter(preferred_month__month=month)

        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        self.send_notification_email(instance)

    def send_notification_email(self, instance):
        subject = f"CIM Industry Experience Zone - Booking {instance.status}"

        context = {
            "booking": instance,
            "month": instance.preferred_month.strftime("%B %Y"),
        }

        template_name = "experience_zone/emails/booking_confirmation.html"
        if instance.status == "Waitlisted":
            template_name = "experience_zone/emails/booking_waitlist.html"

        try:
            html_message = render_to_string(template_name, context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            # Log the error (can extend this to a proper logger)
            print(f"Failed to send email: {e}")


class ExperienceZoneBookingUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceZoneBookingSerializer
    queryset = ExperienceZoneBooking.objects.all()


class ExperienceZoneOccupancyView(APIView):
    def get(self, request, *args, **kwargs):
        # Annotate each month with the number of confirmed bookings
        occupancy_data = (
            ExperienceZoneBooking.objects.values("preferred_month")
            .annotate(
                confirmed_count=Count("id", filter=Q(status="Confirmed")),
                waitlisted_count=Count("id", filter=Q(status="Waitlisted")),
                total_bookings=Count("id"),
            )
            .order_by("preferred_month")
        )

        results = []
        for entry in occupancy_data:
            month_date = entry["preferred_month"]
            confirmed = entry["confirmed_count"]
            results.append(
                {
                    "month": month_date.strftime("%B %Y"),
                    "occupied_seats": confirmed,
                    "remaining_seats": max(0, 50 - confirmed),
                    "waitlisted_count": entry["waitlisted_count"],
                    "is_full": confirmed >= 50,
                }
            )

        return Response(results)
