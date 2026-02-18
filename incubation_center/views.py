from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import IncubationCenter, RescheduleRequest
from .serializers import IncubationCenterSerializer, RescheduleRequestSerializer

# Create your views here.


class IncubationCenterListCreateView(generics.ListCreateAPIView):
    queryset = IncubationCenter.objects.all()
    serializer_class = IncubationCenterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        # Send email to user
        user_subject = "Incubation Center Booking Request Received"
        user_message = render_to_string(
            "incubation_center/user_notification.html", {"instance": instance}
        )
        try:
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
                html_message=user_message,
            )
        except Exception as e:
            print(f"Error sending booking request email to user: {e}")

        # Send email to admin
        admin_subject = "New Incubation Center Booking"
        admin_message = render_to_string(
            "incubation_center/admin_notification.html", {"instance": instance}
        )
        try:
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
                html_message=admin_message,
            )
        except Exception as e:
            print(f"Error sending booking request email to admin: {e}")


class IncubationCenterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IncubationCenter.objects.all()
    serializer_class = IncubationCenterSerializer

    def perform_update(self, serializer):
        # Capture the old status BEFORE saving
        # We access the instance directly from the serializer to get the current DB state
        was_approved = serializer.instance.is_approved
        new_instance = serializer.save()

        # Check if is_approved changed from False to True
        if not was_approved and new_instance.is_approved:
            subject = "Incubation Center Booking Approved"
            message = render_to_string(
                "incubation_center/approval_notification.html",
                {"instance": new_instance},
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [new_instance.email],
                    fail_silently=False,
                    html_message=message,
                )
            except Exception as e:
                print(f"Error sending booking approval email: {e}")


class RescheduleRequestListCreateView(generics.ListCreateAPIView):
    queryset = RescheduleRequest.objects.all()
    serializer_class = RescheduleRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["booking"]

    def perform_create(self, serializer):
        instance = serializer.save()

        # Send email to admin about new reschedule request
        subject = "New Reschedule Request Received"
        message = render_to_string(
            "incubation_center/admin_reschedule_notification.html",
            {"instance": instance},
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
                html_message=message,
            )
        except Exception as e:
            print(f"Error sending reschedule request email to admin: {e}")

        # Send email to user
        user_subject = "Incubation Center Reschedule Request Received"
        user_message = render_to_string(
            "incubation_center/reschedule_request_received.html", {"instance": instance}
        )
        try:
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.booking.email],
                fail_silently=False,
                html_message=user_message,
            )
        except Exception as e:
            print(f"Error sending reschedule request email to user: {e}")


class RescheduleRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RescheduleRequest.objects.all()
    serializer_class = RescheduleRequestSerializer

    def perform_update(self, serializer):
        # Capture the old status BEFORE saving
        old_status = serializer.instance.status
        new_instance = serializer.save()

        # Check if status changed to "Approved"
        if old_status != "Approved" and new_instance.status == "Approved":
            # Update the original booking
            booking = new_instance.booking
            if new_instance.new_booking_date:
                booking.booking_date = new_instance.new_booking_date
            if new_instance.new_start_time:
                booking.start_time = new_instance.new_start_time
            if new_instance.new_end_time:
                booking.end_time = new_instance.new_end_time
            if new_instance.new_room_category:
                booking.room_category = new_instance.new_room_category
            if new_instance.new_booking_type:
                booking.booking_type = new_instance.new_booking_type

            booking.save()

            # Send approval email
            subject = "Incubation Center Reschedule Request Approved"
            message = render_to_string(
                "incubation_center/reschedule_approval.html", {"instance": new_instance}
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [new_instance.booking.email],
                    fail_silently=False,
                    html_message=message,
                )
            except Exception as e:
                print(f"Error sending reschedule approval email: {e}")

        # Check if status changed to "Rejected"
        elif old_status != "Rejected" and new_instance.status == "Rejected":
            # Send rejection email
            subject = "Incubation Center Reschedule Request Rejected"
            message = render_to_string(
                "incubation_center/reschedule_rejection.html",
                {"instance": new_instance},
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [new_instance.booking.email],
                    fail_silently=False,
                    html_message=message,
                )
            except Exception as e:
                print(f"Error sending reschedule rejection email: {e}")
