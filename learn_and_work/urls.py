from django.urls import path

from .views import (
    LearnAndWorkBookingDetailView,
    LearnAndWorkBookingListCreateView,
)

urlpatterns = [
    path(
        "bookings/",
        LearnAndWorkBookingListCreateView.as_view(),
        name="law-booking-list-create",
    ),
    path(
        "bookings/<int:pk>/",
        LearnAndWorkBookingDetailView.as_view(),
        name="law-booking-detail",
    ),
]
