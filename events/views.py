from rest_framework import generics, permissions
from .models import Event, Attendee, Sponsor, AgendaItem
from .serializers import (
    EventListSerializer, EventDetailSerializer, AttendeeSerializer,
    SponsorSerializer, AgendaItemSerializer
)

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventDetailSerializer
        return EventListSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class AttendeeListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs['event_id'])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs['event_id'])
        serializer.save(user=self.request.user, event=event)

class AttendeeRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs['event_id'])

class SponsorListCreateView(generics.ListCreateAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Sponsor.objects.filter(event_id=self.kwargs['event_id'])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs['event_id'])
        serializer.save(event=event)

class SponsorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Sponsor.objects.filter(event_id=self.kwargs['event_id'])

class AgendaItemListCreateView(generics.ListCreateAPIView):
    serializer_class = AgendaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgendaItem.objects.filter(event_id=self.kwargs['event_id'])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs['event_id'])
        serializer.save(event=event)

class AgendaItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgendaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgendaItem.objects.filter(event_id=self.kwargs['event_id'])