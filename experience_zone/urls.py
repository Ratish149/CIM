from django.urls import path

from .views import (
    ExperienceZoneBookingCreateView,
    ExperienceZoneBookingUpdateView,
    ExperienceZoneOccupancyView,
)

urlpatterns = [
    path(
        "bookings/",
        ExperienceZoneBookingCreateView.as_view(),
        name="experience-zone-booking-create",
    ),
    path(
        "bookings/<int:pk>/",
        ExperienceZoneBookingUpdateView.as_view(),
        name="experience-zone-booking-update",
    ),
    path(
        "occupancy/",
        ExperienceZoneOccupancyView.as_view(),
        name="experience-zone-occupancy",
    ),
]
