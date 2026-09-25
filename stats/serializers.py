from rest_framework import serializers


class PlatformStatisticsSerializer(serializers.Serializer):
    wishes_count = serializers.IntegerField(
        help_text="Total number of wishes registered."
    )
    offers_count = serializers.IntegerField(
        help_text="Total number of offers registered."
    )
    upcoming_events_count = serializers.IntegerField(
        help_text="Total number of upcoming published events."
    )
    past_events_count = serializers.IntegerField(
        help_text="Total number of past published events."
    )
    jobs_count = serializers.IntegerField(
        help_text="Total number of published jobs."
    )
    skilled_workforce_roster_count = serializers.IntegerField(
        help_text="Total number of skilled workforce roster / graduates entries."
    )
    work_interest_count = serializers.IntegerField(
        help_text="Total number of work interest entries."
    )
    companies_placing_jobs_count = serializers.IntegerField(
        help_text="Total number of unique companies placing jobs."
    )
    mdmu_registration_count = serializers.IntegerField(
        help_text="Total number of MDMU (Mero Desh Merai Utpadan) registrations."
    )
