from datetime import timedelta
from typing import Any, Dict

from django.db.models import Case, IntegerField, Q, Sum, Value, When
from django.db.models.functions import Coalesce
from django.utils import timezone

from events.models import Event
from jobbriz.models import JobPost, WorkInterest
from jobbriz_institute.models import GraduateRoster
from mero_desh_merai_utpadan.models import MeroDeshMeraiUtpadan
from wish_and_offers.models import Offer, Wish


def get_platform_statistics() -> Dict[str, Any]:
    """
    Fetches aggregate statistics across platform modules:
    - Wishes count
    - Offers count
    - Upcoming events count
    - Past events count
    - Jobs count (taking into account vacancies)
    - Skilled workforce roster / graduates count
    - Work interest count
    - Companies placing jobs count
    - MDMU registrations count
    """
    today = timezone.now().date()

    wishes_count = Wish.objects.count()
    offers_count = Offer.objects.count()

    upcoming_events_count = (
        Event.objects
        .filter(status="Published")
        .filter(
            Q(end_date__gte=today)
            | (Q(end_date__isnull=True) & Q(start_date__gte=today))
        )
        .count()
    )

    past_events_count = (
        Event.objects
        .filter(status="Published")
        .filter(
            Q(end_date__lt=today) | (Q(end_date__isnull=True) & Q(start_date__lt=today))
        )
        .count()
    )

    jobs_count = JobPost.objects.filter(status="Published").aggregate(
        total_vacancies=Coalesce(
            Sum(
                Case(
                    When(no_of_vacancy__gt=0, then="no_of_vacancy"),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            ),
            0,
        )
    )["total_vacancies"]

    skilled_workforce_roster_count = GraduateRoster.objects.count()

    work_interest_count = WorkInterest.objects.count()

    companies_placing_jobs_count = (
        JobPost.objects
        .exclude(company_name__isnull=True)
        .exclude(company_name__exact="")
        .values("company_name")
        .distinct()
        .count()
    )

    mdmu_registration_count = MeroDeshMeraiUtpadan.objects.count()

    return {
        "wishes_count": wishes_count,
        "offers_count": offers_count,
        "upcoming_events_count": upcoming_events_count,
        "past_events_count": past_events_count,
        "jobs_count": jobs_count,
        "skilled_workforce_roster_count": skilled_workforce_roster_count,
        "work_interest_count": work_interest_count,
        "companies_placing_jobs_count": companies_placing_jobs_count,
        "mdmu_registration_count": mdmu_registration_count,
    }


def get_weekly_digest_data(days: int = 7) -> Dict[str, Any]:
    """
    Fetches aggregate and itemized weekly activity data across:
    - Offers created in the past `days`
    - Wishes created in the past `days`
    - Job posts created in the past `days`
    - Events created in the past `days` & upcoming active events
    - Graduates registered in the past `days`
    """
    now = timezone.now()
    start_date = now - timedelta(days=days)
    today = now.date()

    # --- 1. Offers ---
    offers_qs = (
        Offer.objects.filter(created_at__gte=start_date)
        .select_related("event", "user")
        .order_by("-created_at")
    )
    offers_count = offers_qs.count()
    recent_offers = list(offers_qs[:6])

    # --- 2. Wishes ---
    wishes_qs = (
        Wish.objects.filter(created_at__gte=start_date)
        .select_related("event", "user")
        .order_by("-created_at")
    )
    wishes_count = wishes_qs.count()
    recent_wishes = list(wishes_qs[:6])

    # --- 3. Jobs Posted ---
    jobs_qs = (
        JobPost.objects.filter(posted_date__gte=start_date, status="Published")
        .select_related("unit_group")
        .order_by("-posted_date")
    )
    jobs_count = jobs_qs.count()
    recent_jobs = list(jobs_qs[:6])

    # --- 4. Events Created & Upcoming ---
    events_created_qs = (
        Event.objects.filter(created_at__gte=start_date, status="Published")
        .order_by("-created_at")
    )
    events_created_count = events_created_qs.count()
    recent_events_created = list(events_created_qs[:6])

    upcoming_events = list(
        Event.objects.filter(status="Published")
        .filter(
            Q(end_date__gte=today)
            | (Q(end_date__isnull=True) & Q(start_date__gte=today))
        )
        .order_by("start_date")[:4]
    )

    # --- 5. Skilled Graduates ---
    graduates_count = GraduateRoster.objects.filter(created_at__gte=start_date).count()

    return {
        "start_date": start_date,
        "end_date": now,
        "days": days,
        "offers_count": offers_count,
        "recent_offers": recent_offers,
        "wishes_count": wishes_count,
        "recent_wishes": recent_wishes,
        "jobs_count": jobs_count,
        "recent_jobs": recent_jobs,
        "events_created_count": events_created_count,
        "recent_events_created": recent_events_created,
        "upcoming_events": upcoming_events,
        "graduates_count": graduates_count,
        "has_activity": bool(
            offers_count or wishes_count or jobs_count or events_created_count
        ),
    }

