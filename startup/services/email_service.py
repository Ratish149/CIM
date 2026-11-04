import logging
import re
from datetime import date

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def _get_from_email() -> str:
    configured = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", ""
    )
    if "<" in configured and ">" in configured:
        return configured
    return f"CIM Startup & Hackathon <{configured.strip()}>"


def _build_plain_text(html: str) -> str:
    """Clean fallback text from HTML so spam filters don't penalise the email."""
    text = strip_tags(html)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def send_registration_emails(registration) -> None:
    """
    Dispatches two emails after a successful Startup & Hackathon registration:
      1. Admin notification  → ADMIN_EMAIL (always)
      2. User confirmation   → registrant's email (only if provided)

    Both are sent over the same SMTP connection for efficiency.
    """
    current_year = date.today().year
    from_email = _get_from_email()
    admin_email = getattr(settings, "ADMIN_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", None
    )

    context = {
        "registration": registration,
        "contact_name": registration.full_name,
        "current_year": current_year,
    }

    messages = []

    # 1. Admin notification
    if admin_email:
        try:
            admin_html = render_to_string("startup/email_admin_notification.html", context)
            admin_msg = EmailMultiAlternatives(
                subject=f"[Startup & Hackathon] New Registration Received — {registration.full_name} ({registration.get_track_display()})",
                body=_build_plain_text(admin_html),
                from_email=from_email,
                to=[admin_email],
                headers={
                    "X-Auto-Response-Suppress": "OOF, AutoReply",
                    "Auto-Submitted": "auto-generated",
                },
            )
            admin_msg.attach_alternative(admin_html, "text/html")
            messages.append(admin_msg)
        except Exception as exc:
            logger.error(
                f"[Startup & Hackathon] Failed to build admin notification email for registration #{registration.id}: {exc}"
            )
    else:
        logger.warning("[Startup & Hackathon] ADMIN_EMAIL not configured — skipping admin notification.")

    # 2. User confirmation (only when the registrant provided an email)
    user_email = registration.email
    if user_email:
        try:
            user_html = render_to_string("startup/email_user_confirmation.html", context)
            user_msg = EmailMultiAlternatives(
                subject="Your Registration Received — Startup & Hackathon | Birat Expo 2026",
                body=_build_plain_text(user_html),
                from_email=from_email,
                to=[user_email],
                headers={
                    "List-Unsubscribe": f"<mailto:{admin_email}?subject=Unsubscribe>",
                    "Precedence": "bulk",
                    "Auto-Submitted": "auto-generated",
                    "X-Auto-Response-Suppress": "OOF, AutoReply",
                },
            )
            user_msg.attach_alternative(user_html, "text/html")
            messages.append(user_msg)
        except Exception as exc:
            logger.error(
                f"[Startup & Hackathon] Failed to build user confirmation email for registration #{registration.id}: {exc}"
            )
    else:
        logger.info(
            f"[Startup & Hackathon] No user email provided for registration #{registration.id} — skipping user confirmation."
        )

    if not messages:
        return

    # Send all messages over one SMTP connection
    connection = get_connection()
    try:
        connection.open()
        sent = connection.send_messages(messages)
        logger.info(
            f"[Startup & Hackathon] Sent {sent}/{len(messages)} email(s) for registration #{registration.id}."
        )
    except Exception as exc:
        logger.error(
            f"[Startup & Hackathon] SMTP error when sending emails for registration #{registration.id}: {exc}"
        )
    finally:
        try:
            connection.close()
        except Exception:
            pass
