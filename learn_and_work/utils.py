import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_learn_and_work_emails(booking):
    """
    Send two emails after a LearnAndWorkBooking is created:
      1. Acknowledgement to the user/teacher (only if email was provided).
      2. Full admin notification to ADMIN_EMAIL.
    """
    context = {"booking": booking}
    _send_user_acknowledgement(booking, context)
    _send_admin_notification(booking, context)


def _send_user_acknowledgement(booking, context):
    """Send a 'request received — pending confirmation' email to the teacher."""
    if not booking.email:
        return

    subject = "Learn & Work Platform — Booking Request Received | Birat Expo 2026"

    try:
        html_body = render_to_string("learn_and_work/user_acknowledgement.html", context)
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        logger.info("Learn & Work: acknowledgement sent to %s", booking.email)
    except Exception as exc:
        logger.error(
            "Learn & Work: failed to send acknowledgement to %s — %s",
            booking.email,
            exc,
        )


def _send_admin_notification(booking, context):
    """Send a detailed booking summary to the admin."""
    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    if not admin_email:
        logger.warning("Learn & Work: ADMIN_EMAIL not set — skipping admin notification.")
        return

    subject = (
        f"[Learn & Work] New Booking Request — {booking.school} | "
        f"{booking.zone} | {booking.date} {booking.time}"
    )

    try:
        html_body = render_to_string("learn_and_work/admin_notification.html", context)
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        logger.info("Learn & Work: admin notification sent to %s", admin_email)
    except Exception as exc:
        logger.error("Learn & Work: failed to send admin notification — %s", exc)
