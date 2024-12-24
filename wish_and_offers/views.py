# wish_and_offers/views.py

from rest_framework import generics, permissions
from .models import Wish, Offer, Match, Product, Service, Category
from .serializers import WishSerializer, OfferSerializer, MatchSerializer, ProductSerializer, ServiceSerializer, CategorySerializer
from events.models import Event
from rest_framework.response import Response
from rest_framework import status

class WishListCreateView(generics.ListCreateAPIView):
    serializer_class = WishSerializer

    def get_queryset(self):
        event_slug = self.kwargs.get('event_slug')
        if event_slug:
            return Wish.objects.filter(event__slug=event_slug).order_by('created_at')
        return Wish.objects.all().order_by('created_at')

    def perform_create(self, serializer):
        event_id = self.request.data.get('event_id')
        event = Event.objects.get(pk=event_id) if event_id else None
        serializer.save(event=event)

class WishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer

    def get(self, request, *args, **kwargs):
        wish_id = self.kwargs.get('pk')
        matched_offers = Match.objects.filter(wish_id=wish_id)
        serializer = MatchSerializer(matched_offers, many=True)
        return Response(serializer.data)


class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        event_slug = self.kwargs.get('event_slug')
        if event_slug:
            return Offer.objects.filter(event__slug=event_slug).order_by('created_at')
        return Offer.objects.all().order_by('created_at')

    def perform_create(self, serializer):
        event_id = self.request.data.get('event_id')
        event = Event.objects.get(pk=event_id) if event_id else None
        serializer.save(event=event)

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('pk')
        matched_wishes = Match.objects.filter(offer_id=offer_id)
        serializer = MatchSerializer(matched_wishes, many=True)
        return Response(serializer.data)


class MatchListView(generics.ListAPIView):
    queryset = Match.objects.all().order_by('id')
    serializer_class = MatchSerializer

    def get_queryset(self):
        wish_id = self.request.query_params.get('wish_id')
        offer_id = self.request.query_params.get('offer_id')
        
        if wish_id:
            return Match.objects.filter(wish_id=wish_id).order_by('id')
        elif offer_id:
            return Match.objects.filter(offer_id=offer_id).order_by('id')
        
        return super().get_queryset()  # Return all matches if no filters are applied

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer