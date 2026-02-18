from django.urls import path

from .views import (
    IncubationCenterDetailView,
    IncubationCenterListCreateView,
    RescheduleRequestDetailView,
    RescheduleRequestListCreateView,
)

urlpatterns = [
    path(
        "incubation-center/",
        IncubationCenterListCreateView.as_view(),
        name="incubation-center-list-create",
    ),
    path(
        "incubation-center/<int:pk>/",
        IncubationCenterDetailView.as_view(),
        name="incubation-center-detail",
    ),
    path(
        "reschedule-request/",
        RescheduleRequestListCreateView.as_view(),
        name="reschedule-request-list-create",
    ),
    path(
        "reschedule-request/<int:pk>/",
        RescheduleRequestDetailView.as_view(),
        name="reschedule-request-detail",
    ),
]
