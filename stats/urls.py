from django.urls import path

from stats.views import PlatformStatisticsView

urlpatterns = [
    path("", PlatformStatisticsView.as_view(), name="platform-statistics"),
]
