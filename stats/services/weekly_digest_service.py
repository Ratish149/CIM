import logging
import smtplib
import time
from datetime import date
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

from accounts.models import CustomUser
from stats.selectors.stats_selector import get_weekly_digest_data

logger = logging.getLogger(__name__)

# Daily sending limits enforced by Google SMTP
GMAIL_DAILY_RECIPIENT_LIMIT = 500


def _format_from_email() -> str:
    """
    Ensures the from_email has a professional display name to reduce spam scoring.
    Example: 'Biratbazaar <info.cimbrt@gmail.com>'
    """
    configured_from = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", "info.cimbrt@gmail.com"
    )
    if "<" in configured_from and ">" in configured_from:
        return configured_from
    return f"Biratbazaar <{configured_from.strip()}>"


def _build_plain_text_digest(
    recipient_name: str,
    week_range: str,
    stats: Dict[str, Any],
    unsubscribe_url: str,
) -> str:
    """
    Builds a clean, human-readable plain text version of the weekly digest.
    Spam filters penalize emails whose text/plain fallback is garbled or missing.
    """
    lines = [
        "Chamber of Industries Morang - Weekly Biratbazaar Highlights",
        f"Period: {week_range}",
        "",
        f"Hello {recipient_name},",
        "",
        "Here is what transpired across the platform in the past 7 days:",
        "",
        "--- PLATFORM SNAPSHOT ---",
        f"- New Offers: {stats.get('offers_count', 0)}",
        f"- New Wishes: {stats.get('wishes_count', 0)}",
        f"- Jobs Posted: {stats.get('jobs_count', 0)}",
        f"- Events Created: {stats.get('events_created_count', 0)}",
        f"- Skilled Graduates: {stats.get('graduates_count', 0)}",
        "",
    ]

    recent_offers = stats.get("recent_offers", [])
    if recent_offers:
        lines.append("--- NEW OFFERS ---")
        for offer in recent_offers[:4]:
            user_title = offer.user.get_full_name() if offer.user else "Verified Seller"
            lines.append(f"• {offer.title} (by {user_title})")
        lines.append("Explore offers: https://biratbazaar.com/wishes-and-offers")
        lines.append("")

    recent_wishes = stats.get("recent_wishes", [])
    if recent_wishes:
        lines.append("--- NEW BUYER WISHES ---")
        for wish in recent_wishes[:4]:
            user_title = wish.user.get_full_name() if wish.user else "Verified Buyer"
            lines.append(f"• {wish.title} (by {user_title})")
        lines.append("Explore wishes: https://biratbazaar.com/wishes-and-offers")
        lines.append("")

    recent_jobs = stats.get("recent_jobs", [])
    if recent_jobs:
        lines.append("--- RECENT CAREER OPENINGS ---")
        for job in recent_jobs[:4]:
            company = job.company_name or "Industrial Partner"
            lines.append(f"• {job.title} at {company}")
        lines.append("View jobs: https://biratbazaar.com/jobbriz")
        lines.append("")

    upcoming_events = stats.get("upcoming_events", [])
    if upcoming_events:
        lines.append("--- UPCOMING EXPOS & TRADE EVENTS ---")
        for ev in upcoming_events[:3]:
            loc = f" ({ev.location})" if ev.location else ""
            lines.append(f"• {ev.title}{loc}")
        lines.append("Event calendar: https://biratbazaar.com/events")
        lines.append("")

    lines.extend([
        "---",
        "Visit Biratbazaar: https://biratbazaar.com/",
        "Chamber of Industries Morang (CIM), Biratnagar, Koshi Province, Nepal.",
        "",
        "You received this email because you are a registered member of Biratbazaar.",
        f"To unsubscribe or update your email preferences, visit: {unsubscribe_url}",
    ])

    return "\n".join(lines)


def send_weekly_digest(
    days: int = 7,
    test_email: Optional[str] = None,
    dry_run: bool = False,
    batch_size: int = 25,
    delay_between_batches: float = 1.5,
) -> Dict[str, Any]:
    """
    Collects weekly platform activity and dispatches the digest email.
    Sends 1-to-1 individual emails with rate throttling to prevent Gmail SMTP burst blocks.
    Reuses a persistent connection across batches for performance.
    """
    stats_data = get_weekly_digest_data(days=days)
    current_year = date.today().year

    start_str = stats_data["start_date"].strftime("%b %d")
    end_str = stats_data["end_date"].strftime("%b %d, %Y")
    week_range = f"{start_str} - {end_str}"

    recipients: List[Dict[str, str]] = []

    if test_email:
        recipients.append({
            "email": test_email.strip(),
            "name": "Valued Member",
        })
    else:
        users = (
            CustomUser.objects
            .filter(is_active=True)
            .exclude(email="")
            .exclude(email__isnull=True)
            .only("email", "first_name", "last_name", "username")
        )
        seen_emails = set()
        for u in users:
            clean_email = u.email.strip().lower()
            if clean_email and clean_email not in seen_emails:
                seen_emails.add(clean_email)
                full_name = f"{u.first_name} {u.last_name}".strip()
                recipients.append({
                    "email": u.email.strip(),
                    "name": full_name or u.username or "Member",
                })

    total_recipients = len(recipients)
    sent_count = 0
    failed_count = 0

    # Gmail SMTP daily limit sanity check
    is_gmail = "gmail" in getattr(settings, "EMAIL_HOST", "").lower()
    if is_gmail and total_recipients > GMAIL_DAILY_RECIPIENT_LIMIT:
        logger.warning(
            f"Target recipient count ({total_recipients}) exceeds Gmail free SMTP limit "
            f"({GMAIL_DAILY_RECIPIENT_LIMIT}/day). Gmail may reject messages once the quota is reached."
        )

    if dry_run:
        logger.info(
            f"[DRY RUN] Weekly digest prepared for {total_recipients} individual recipients. "
            f"Batch size: {batch_size}, Delay: {delay_between_batches}s. "
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

    if not recipients:
        logger.info("No recipients found for weekly digest.")
        return {
            "dry_run": False,
            "total_recipients": 0,
            "sent_count": 0,
            "failed_count": 0,
            "stats": stats_data,
        }

    from_email = _format_from_email()
    subject = f"Weekly Biratbazaar Highlights ({week_range})"

    connection = get_connection()
    try:
        connection.open()
    except Exception as exc:
        logger.error(f"Failed to open SMTP connection: {exc}")
        return {
            "dry_run": False,
            "total_recipients": total_recipients,
            "sent_count": 0,
            "failed_count": total_recipients,
            "stats": stats_data,
        }

    total_batches = (total_recipients + batch_size - 1) // batch_size
    quota_exhausted = False

    try:
        for i in range(0, total_recipients, batch_size):
            if quota_exhausted:
                remaining = total_recipients - (sent_count + failed_count)
                failed_count += remaining
                logger.error(f"Skipping remaining {remaining} recipients due to quota exhaustion.")
                break

            batch = recipients[i : i + batch_size]
            batch_idx = (i // batch_size) + 1
            messages_to_send: List[EmailMultiAlternatives] = []

            for recipient in batch:
                recipient_email = recipient["email"]
                recipient_name = recipient["name"]
                unsubscribe_url = f"https://biratbazaar.com/unsubscribe?email={recipient_email}"

                context = {
                    "recipient_name": recipient_name,
                    "week_range": week_range,
                    "current_year": current_year,
                    "stats": stats_data,
                    "unsubscribe_url": unsubscribe_url,
                }
                html_content = render_to_string("stats/weekly_digest.html", context)
                plain_text = _build_plain_text_digest(
                    recipient_name=recipient_name,
                    week_range=week_range,
                    stats=stats_data,
                    unsubscribe_url=unsubscribe_url,
                )

                headers = {
                    "List-Unsubscribe": f"<https://biratbazaar.com/unsubscribe?email={recipient_email}>, <mailto:info.cimbrt@gmail.com?subject=Unsubscribe%20{recipient_email}>",
                    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
                    "Precedence": "bulk",
                    "Auto-Submitted": "auto-generated",
                    "X-Auto-Response-Suppress": "OOF, AutoReply",
                }

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_text,
                    from_email=from_email,
                    to=[recipient_email],
                    headers=headers,
                    connection=connection,
                )
                msg.attach_alternative(html_content, "text/html")
                messages_to_send.append(msg)

            try:
                sent = connection.send_messages(messages_to_send)
                sent_count += sent
                failed_count += len(messages_to_send) - sent
                logger.info(
                    f"Dispatched weekly digest batch {batch_idx}/{total_batches} "
                    f"({sent}/{len(messages_to_send)} delivered)."
                )
            except smtplib.SMTPDataError as err:
                failed_count += len(messages_to_send)
                logger.error(f"SMTP Data error in batch {batch_idx}: {err}")
                if err.smtp_code == 550 or "quota" in str(err).lower():
                    logger.critical("Gmail daily sending quota has been reached! Halting further sends.")
                    quota_exhausted = True
            except Exception as exc:
                failed_count += len(messages_to_send)
                logger.error(f"Failed to dispatch batch {batch_idx}/{total_batches}: {exc}")

            # Throttling between batches to avoid burst rate limiting from Gmail SMTP
            if delay_between_batches > 0 and batch_idx < total_batches and not quota_exhausted:
                time.sleep(delay_between_batches)

    finally:
        try:
            connection.close()
        except Exception:
            pass

    return {
        "dry_run": False,
        "total_recipients": total_recipients,
        "sent_count": sent_count,
        "failed_count": failed_count,
        "stats": stats_data,
        "quota_exhausted": quota_exhausted,
    }
