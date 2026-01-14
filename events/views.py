from rest_framework import generics, permissions

from .models import AgendaItem, Attendee, Event, Sponsor
from .serializers import (
    AgendaItemSerializer,
    AttendeeSerializer,
    EventCreateSerializer,
    EventDetailSerializer,
    EventListSerializer,
    SponsorSerializer,
)


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(status="Published").order_by("order")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        return EventListSerializer

    def perform_create(self, serializer):
        serializer.save()


class GetFeaturedEvents(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(status="Published", is_featured=True).order_by(
            "order"
        )


class GetPopularEvents(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(status="Published", is_popular=True).order_by(
            "order"
        )


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class AttendeeListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs["event_id"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_id"])
        serializer.save(user=self.request.user, event=event)


class AttendeeRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs["event_id"])


class SponsorListCreateView(generics.ListCreateAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Sponsor.objects.filter(event_id=self.kwargs["event_id"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_id"])
        serializer.save(event=event)


class SponsorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Sponsor.objects.filter(event_id=self.kwargs["event_id"])


class AgendaItemListCreateView(generics.ListCreateAPIView):
    serializer_class = AgendaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgendaItem.objects.filter(event_id=self.kwargs["event_id"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_id"])
        serializer.save(event=event)


class AgendaItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgendaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgendaItem.objects.filter(event_id=self.kwargs["event_id"])
