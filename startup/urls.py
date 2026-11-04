from django.urls import path

from startup.views import (
    StartUpRegistrationDetailView,
    StartUpRegistrationListCreateView,
)

urlpatterns = [
    path(
        "registrations/",
        StartUpRegistrationListCreateView.as_view(),
        name="startup-registration-list-create",
    ),
    path(
        "registrations/<int:pk>/",
        StartUpRegistrationDetailView.as_view(),
        name="startup-registration-detail",
    ),
]
