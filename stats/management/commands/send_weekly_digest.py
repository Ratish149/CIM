from django.core.management.base import BaseCommand

from stats.services.weekly_digest_service import send_weekly_digest


class Command(BaseCommand):
    help = (
        "Collects weekly platform updates (offers, wishes, jobs, events, stats) "
        "and emails a personalized digest directly to registered users with rate limiting."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate the command without sending any emails.",
        )
        parser.add_argument(
            "--test-email",
            type=str,
            default=None,
            help="Send the weekly digest only to this test email address.",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Number of days to include in the digest (default: 7).",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=25,
            help="Number of individual recipient emails sent per SMTP batch (default: 25).",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=1.5,
            help="Pause in seconds between batches to avoid SMTP rate limiting (default: 1.5).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        test_email = options["test_email"]
        days = options["days"]
        batch_size = options["batch_size"]
        delay = options["delay"]

        self.stdout.write(
            self.style.NOTICE(
                f"Starting weekly digest (Window: last {days} days, Dry-run: {dry_run}, "
                f"Test: {test_email or 'All active users'}, Batch: {batch_size}, Delay: {delay}s)..."
            )
        )

        result = send_weekly_digest(
            days=days,
            test_email=test_email,
            dry_run=dry_run,
            batch_size=batch_size,
            delay_between_batches=delay,
        )

        stats = result["stats"]
        self.stdout.write("--- Weekly Activity Summary ---")
        self.stdout.write(f"- New Offers: {stats['offers_count']}")
        self.stdout.write(f"- New Wishes: {stats['wishes_count']}")
        self.stdout.write(f"- New Jobs Posted: {stats['jobs_count']}")
        self.stdout.write(f"- Events Created: {stats['events_created_count']}")
        self.stdout.write(f"- Active Upcoming Events: {len(stats['upcoming_events'])}")

        if result["dry_run"]:
            self.stdout.write(
                self.style.WARNING(
                    f"[DRY-RUN] Processed {result['total_recipients']} recipients without dispatching."
                )
            )
        elif result.get("quota_exhausted"):
            self.stdout.write(
                self.style.ERROR(
                    f"Process stopped early! Daily SMTP quota was reached. "
                    f"Sent: {result['sent_count']}, Failed: {result['failed_count']}."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Completed: {result['sent_count']}/{result['total_recipients']} emails sent successfully "
                    f"({result['failed_count']} failed)."
                )
            )
