from django.core.management.base import BaseCommand

from stats.services.weekly_digest_service import send_weekly_digest


class Command(BaseCommand):
    help = (
        "Collects weekly platform updates (offers, wishes, jobs, events, stats) "
        "and emails a digest to all registered users."
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
            default=50,
            help="Number of recipients per BCC batch (default: 50).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        test_email = options["test_email"]
        days = options["days"]
        batch_size = options["batch_size"]

        self.stdout.write(
            self.style.NOTICE(
                f"Starting weekly digest (Window: last {days} days, Dry-run: {dry_run}, Test: {test_email or 'None'}, BCC Batch Size: {batch_size})..."
            )
        )

        result = send_weekly_digest(
            days=days,
            test_email=test_email,
            dry_run=dry_run,
            batch_size=batch_size,
        )

        stats = result["stats"]
        self.stdout.write("--- Weekly Activity Summary ---")
        self.stdout.write(f"- New Offers: {stats['offers_count']}")
        self.stdout.write(f"- New Wishes: {stats['wishes_count']}")
        self.stdout.write(f"- New Jobs Posted: {stats['jobs_count']}")
        self.stdout.write(f"- Events Created: {stats['events_created_count']}")
        self.stdout.write(f"- Active Upcoming Events: {len(stats['upcoming_events'])}")
        self.stdout.write(f"- New Skilled Graduates: {stats['graduates_count']}")
        self.stdout.write("-------------------------------")

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"[DRY RUN COMPLETE] Found {result['total_recipients']} eligible user(s). No emails were dispatched."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Weekly digest dispatched successfully! Sent: {result['sent_count']}, Failed: {result['failed_count']} (Total targeted: {result['total_recipients']})"
                )
            )
