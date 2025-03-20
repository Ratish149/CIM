from django.urls import path
from .views import (
    RegistrationView,
    AvailableSessionsView,
    TimeSlotByDateView,
    RegistrationDetailView,
    UpdateAttendanceView,
)

urlpatterns = [
    path("registrations/", RegistrationView.as_view(), name="registration-list"),
    path(
        "registrations/available-sessions/",
        AvailableSessionsView.as_view(),
        name="available-sessions",
    ),
    path(
        "registrations/<int:pk>/",
        RegistrationDetailView.as_view(),
        name="registration-detail",
    ),
    path("timeslots/", TimeSlotByDateView.as_view(), name="timeslot-by-date"),
    path('registrations/<int:pk>/attendance/', UpdateAttendanceView.as_view(), name='update-attendance'),
]
