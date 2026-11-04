from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from startup.filters import StartUpRegistrationFilter
from startup.models import StartUpRegistration
from startup.serializers import (
    StartUpRegistrationListSerializer,
    StartUpRegistrationSerializer,
)


class StartUpRegistrationListCreateView(ListCreateAPIView):
    """
    GET  /api/startup/registrations/     — List all enquiries (admin/staff only)
    POST /api/startup/registrations/     — Submit a new BIC Pavilion enquiry (public)
    """

    queryset = StartUpRegistration.objects.only(
        "id",
        "track",
        "status",
        "full_name",
        "phone",
        "email",
        "organization_name",
        "role",
        "municipality",
        "heard_about_us",
        "consent",
        "keep_updated",
        "created_at",
    ).order_by("-created_at")
    filterset_class = StartUpRegistrationFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StartUpRegistrationListSerializer
        return StartUpRegistrationSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class StartUpRegistrationDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET    /api/startup/registrations/<id>/   — Retrieve full record
    PATCH  /api/startup/registrations/<id>/   — Partial update (status, etc.)
    DELETE /api/startup/registrations/<id>/   — Delete an enquiry
    """

    queryset = StartUpRegistration.objects.all()
    serializer_class = StartUpRegistrationSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "patch", "delete", "head", "options"]
