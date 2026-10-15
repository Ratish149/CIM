import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_thematic_registration_emails(registration) -> None:
    """
    Sends email notifications upon new thematic session registration:
    1. Confirmation email to the participant (thank you for submitting / application received).
    2. Alert email to CIM administration.
    """
    try:
        from_email = (
            getattr(settings, "DEFAULT_FROM_EMAIL", None) or "info.cimbrt@gmail.com"
        )
        sessions = registration.sessions.all()

        context = {
            "registration": registration,
            "sessions": sessions,
        }

        # 1. Send confirmation email to the participant
        if registration.email:
            participant_subject = (
                "Application Received: CIM Thematic Session Registration"
            )
            participant_html = render_to_string(
                "stall_booking/emails/thematic_registration_participant.html",
                context,
            )
            participant_text = strip_tags(participant_html)

            participant_email = EmailMultiAlternatives(
                subject=participant_subject,
                body=participant_text,
                from_email=from_email,
                to=[registration.email],
            )
            participant_email.attach_alternative(participant_html, "text/html")
            participant_email.send(fail_silently=True)

        # 2. Send alert email to CIM / Admin
        admin_email = getattr(settings, "ADMIN_EMAIL", None) or "info.cimbrt@gmail.com"
        if admin_email:
            admin_subject = f"ADMIN ALERT: New Thematic Session Registration - {registration.name} ({registration.organization})"
            admin_html = render_to_string(
                "stall_booking/emails/thematic_registration_admin.html",
                context,
            )
            admin_text = strip_tags(admin_html)

            admin_recipients = (
                [admin_email] if isinstance(admin_email, str) else list(admin_email)
            )
            admin_msg = EmailMultiAlternatives(
                subject=admin_subject,
                body=admin_text,
                from_email=from_email,
                to=admin_recipients,
            )
            admin_msg.attach_alternative(admin_html, "text/html")
            admin_msg.send(fail_silently=True)

    except Exception as exc:
        logger.error(
            f"Failed to send thematic registration email for registration ID {getattr(registration, 'id', None)}: {exc}",
            exc_info=True,
        )
