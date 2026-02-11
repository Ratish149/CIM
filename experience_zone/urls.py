from django.urls import path

from .views import ExperienceZoneBookingCreateView, ExperienceZoneOccupancyView

urlpatterns = [
    path(
        "bookings/",
        ExperienceZoneBookingCreateView.as_view(),
        name="experience-zone-booking-create",
    ),
    path(
        "occupancy/",
        ExperienceZoneOccupancyView.as_view(),
        name="experience-zone-occupancy",
    ),
]
