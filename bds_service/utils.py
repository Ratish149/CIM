import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_bds_connect_emails(registration):
    """
    Send two emails after a BDSConnect registration:
      1. Confirmation email to the registrant (only if they provided an email).
      2. Admin notification email to ADMIN_EMAIL.
    """
    context = {"registration": registration}

    _send_user_confirmation(registration, context)
    _send_admin_notification(registration, context)


def _send_user_confirmation(registration, context):
    """Send confirmation to the registrant if they provided an email address."""
    if not registration.email:
        return

    if registration.track == "business":
        subject = "Your BDS Connect Pavilion Registration — Birat Expo 2026"
    else:
        subject = "BDS Connect Pavilion — Provider Registration Received"

    try:
        html_body = render_to_string("bds_service/user_confirmation.html", context)
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[registration.email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        logger.info("BDS Connect: user confirmation sent to %s", registration.email)
    except Exception as exc:
        logger.error(
            "BDS Connect: failed to send user confirmation to %s — %s",
            registration.email,
            exc,
        )


def _send_admin_notification(registration, context):
    """Send a detailed notification to the admin email."""
    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    if not admin_email:
        logger.warning(
            "BDS Connect: ADMIN_EMAIL is not set in settings — skipping admin notification."
        )
        return

    if registration.track == "business":
        subject = f"[BDS Connect] New Business Registration — {registration.name}"
    else:
        subject = f"[BDS Connect] New Provider Registration — {registration.name} ({registration.business_name})"

    try:
        html_body = render_to_string("bds_service/admin_notification.html", context)
        email = EmailMessage(
            subject=subject,
            body=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        logger.info("BDS Connect: admin notification sent to %s", admin_email)
    except Exception as exc:
        logger.error("BDS Connect: failed to send admin notification — %s", exc)
