# wish_and_offers/views.py

from rest_framework import generics, permissions
from .models import Wish, Offer, Match
from .serializers import WishSerializer, OfferSerializer, MatchSerializer
from events.models import Event

class WishListCreateView(generics.ListCreateAPIView):
    serializer_class = WishSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return Wish.objects.filter(event_id=event_id).order_by('created_at')  # Filter by event_id
        return Wish.objects.all().order_by('created_at')  # Return all wishes if no event_id

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id) if event_id else None
        serializer.save(event=event)  # Save only the event

class WishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return Offer.objects.filter(event_id=event_id).order_by('created_at')  # Filter by event_id
        return Offer.objects.all().order_by('created_at')  # Return all offers if no event_id

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id) if event_id else None
        serializer.save(event=event)  # Save only the event

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

class MatchListView(generics.ListAPIView):
    queryset = Match.objects.all()  # Get all matches
    serializer_class = MatchSerializer  # Use the MatchSerializer