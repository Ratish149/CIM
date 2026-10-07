import logging
from datetime import date
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.models import CustomUser
from stats.selectors.stats_selector import get_weekly_digest_data

logger = logging.getLogger(__name__)


def send_weekly_digest(
    days: int = 7,
    test_email: Optional[str] = None,
    dry_run: bool = False,
    batch_size: int = 50,
) -> Dict[str, Any]:
    """
    Collects weekly platform activity and dispatches the digest email
    using BCC in batches to protect user privacy and respect SMTP limits.
    """
    stats_data = get_weekly_digest_data(days=days)
    current_year = date.today().year

    start_str = stats_data["start_date"].strftime("%b %d")
    end_str = stats_data["end_date"].strftime("%b %d, %Y")
    week_range = f"{start_str} - {end_str}"

    if test_email:
        recipient_emails = [test_email.strip()]
    else:
        users = (
            CustomUser.objects
            .filter(is_active=True)
            .exclude(email="")
            .exclude(email__isnull=True)
            .values_list("email", flat=True)
        )
        # Deduplicate and normalize
        recipient_emails = list(
            dict.fromkeys(e.strip() for e in users if e and e.strip())
        )

    total_recipients = len(recipient_emails)
    sent_count = 0
    failed_count = 0

    if dry_run:
        logger.info(
            f"[DRY RUN] Weekly digest prepared for {total_recipients} users (BCC batch size: {batch_size}). "
            f"Offers: {stats_data['offers_count']}, Wishes: {stats_data['wishes_count']}, "
            f"Jobs: {stats_data['jobs_count']}, Events: {stats_data['events_created_count']}"
        )
        return {
            "dry_run": True,
            "total_recipients": total_recipients,
            "sent_count": 0,
            "failed_count": 0,
            "stats": stats_data,
        }

    if not recipient_emails:
        logger.info("No recipients found for weekly digest.")
        return {
            "dry_run": False,
            "total_recipients": 0,
            "sent_count": 0,
            "failed_count": 0,
            "stats": stats_data,
        }

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", "info.cimbrt@gmail.com"
    )
    subject = f"Weekly Platform Highlights ({week_range})"

    # Render template once for all BCC recipients
    context = {
        "recipient_name": "Member",
        "week_range": week_range,
        "current_year": current_year,
        "stats": stats_data,
    }
    html_content = render_to_string("stats/weekly_digest.html", context)
    text_content = strip_tags(html_content)

    # Dispatch in batches using BCC
    total_batches = (total_recipients + batch_size - 1) // batch_size
    for i in range(0, total_recipients, batch_size):
        batch = recipient_emails[i : i + batch_size]
        batch_idx = (i // batch_size) + 1

        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[from_email],
                bcc=batch,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            sent_count += len(batch)
            logger.info(
                f"Dispatched weekly digest batch {batch_idx}/{total_batches} "
                f"({len(batch)} recipients in BCC)."
            )
        except Exception as exc:
            failed_count += len(batch)
            logger.error(
                f"Failed to dispatch weekly digest batch {batch_idx}/{total_batches} "
                f"({len(batch)} recipients): {exc}"
            )

    return {
        "dry_run": False,
        "total_recipients": total_recipients,
        "sent_count": sent_count,
        "failed_count": failed_count,
        "stats": stats_data,
    }
