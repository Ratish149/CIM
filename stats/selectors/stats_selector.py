from typing import Any, Dict

from django.db.models import Q
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
    - Jobs count
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

    jobs_count = JobPost.objects.filter(status="Published").count()

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
