from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BDSCategory, BDSConnect, BDSService, Tags
from .serializers import (
    BDSCategorySerializer,
    BDSConnectSerializer,
    BDSServiceSerializer,
    TagsSerializer,
)
from .utils import send_bds_connect_emails

# ── BDSCategory ───────────────────────────────────────────────────────────────


class BDSCategoryListCreateView(generics.ListCreateAPIView):
    queryset = BDSCategory.objects.all()
    serializer_class = BDSCategorySerializer


class BDSCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BDSCategory.objects.all()
    serializer_class = BDSCategorySerializer


# ── Tags ──────────────────────────────────────────────────────────────────────


class TagsListCreateView(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class TagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


# ── BDSService ────────────────────────────────────────────────────────────────


class BDSServiceListCreateView(generics.ListCreateAPIView):
    queryset = BDSService.objects.all()
    serializer_class = BDSServiceSerializer


class BDSServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BDSService.objects.all()
    serializer_class = BDSServiceSerializer


# ── BDSConnect ────────────────────────────────────────────────────────────────


class BDSConnectCreateView(generics.CreateAPIView):
    """
    POST /api/bds/connect/
    Public endpoint — no authentication required.
    Accepts registration submissions from both the Business and Provider form tabs.
    """

    queryset = BDSConnect.objects.all()
    serializer_class = BDSConnectSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Send emails to user and admin
        send_bds_connect_emails(serializer.instance)
        return Response(
            {
                "detail": "Registration submitted successfully.",
                "id": serializer.instance.id,
                "track": serializer.instance.track,
                "name": serializer.instance.name,
            },
            status=status.HTTP_201_CREATED,
        )


class BDSConnectListView(generics.ListAPIView):
    """
    GET /api/bds/connect/
    Returns all registrations. Add authentication/permissions as needed.
    Supports ?track=business or ?track=provider filtering.
    """

    serializer_class = BDSConnectSerializer

    def get_queryset(self):
        qs = BDSConnect.objects.all()
        track = self.request.query_params.get("track")
        if track in (BDSConnect.TRACK_BUSINESS, BDSConnect.TRACK_PROVIDER):
            qs = qs.filter(track=track)
        return qs


class BDSConnectDetailView(generics.RetrieveDestroyAPIView):
    """
    GET  /api/bds/connect/<id>/
    DELETE /api/bds/connect/<id>/
    """

    queryset = BDSConnect.objects.all()
    serializer_class = BDSConnectSerializer
