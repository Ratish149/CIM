# wish_and_offers/views.py

from rest_framework import generics, permissions
from .models import Wish, Offer
from .serializers import WishSerializer, OfferSerializer
from events.models import Event

class WishListCreateView(generics.ListCreateAPIView):
    serializer_class = WishSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return Wish.objects.filter(event_id=event_id)
        return Wish.objects.all()

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id) if event_id else None
        serializer.save(user=self.request.user, event=event)

class WishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    permission_classes = [permissions.IsAuthenticated]

class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer


    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if event_id:
            return Offer.objects.filter(event_id=event_id)
        return Offer.objects.all()

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(pk=event_id) if event_id else None
        serializer.save(user=self.request.user, event=event)

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]