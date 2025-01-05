# wish_and_offers/views.py

from rest_framework import generics, permissions
from .models import Wish, Offer, Match, Service, Category, HSCode
from .serializers import (
    WishSerializer, 
    OfferSerializer, 
    MatchSerializer, 
    ServiceSerializer, 
    CategorySerializer, 
    HSCodeSerializer,
    WishWithOffersSerializer,
    OfferWithWishesSerializer,
    HSCodeFileUploadSerializer
)
from events.models import Event
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import csv
from rest_framework import filters
from django.db.models import Q

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
        wish = serializer.save(event=event)  # Capture the created wish and its matches
        
        # Retrieve matches for the created wish
        match_objects = Match.objects.filter(wish=wish)
        return Response({
            'wish': WishWithOffersSerializer(wish).data,
            'matches': MatchSerializer(match_objects, many=True).data  # Serialize the matches
        }, status=status.HTTP_201_CREATED)

class WishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer

    def get(self, request, *args, **kwargs):
        wish_id = self.kwargs.get('pk')
        # Retrieve the specific wish object
        wish = self.get_object()  # This will use the default behavior to get the wish by ID
        # Use the new serializer to get wish with offers
        wish_serializer = WishWithOffersSerializer(wish)
        
        return Response(wish_serializer.data)


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
        offer = serializer.save(event=event)  # Capture the created offer and its matches
        
        # Retrieve matches for the created offer
        match_objects = Match.objects.filter(offer=offer)
        return Response({
            'offer': OfferWithWishesSerializer(offer).data,
            'matches': MatchSerializer(match_objects, many=True).data  # Serialize the matches
        }, status=status.HTTP_201_CREATED)

class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        offer_id = self.kwargs.get('pk')
        # Retrieve the specific offer object
        offer = self.get_object()  # This will use the default behavior to get the offer by ID
        # Use the new serializer to get offer with wishes
        offer_serializer = OfferWithWishesSerializer(offer)
        
        return Response(offer_serializer.data)


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

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

class HSCodeListView(generics.ListAPIView):
    queryset = HSCode.objects.all().order_by('hs_code')
    serializer_class = HSCodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['hs_code', 'description']
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_queryset(self):
        queryset = HSCode.objects.all().order_by('hs_code')
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            # If the search query contains only numbers, do a prefix search on hs_code
            if search_query.isdigit():
                queryset = queryset.filter(hs_code__startswith=search_query)
            else:
                # If the search contains text, search in both hs_code and description
                queryset = queryset.filter(
                    Q(hs_code__icontains=search_query) |
                    Q(description__icontains=search_query)
                )
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response(
                {"error": "No matching HS codes found"},
                status=status.HTTP_404_NOT_FOUND
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class HSCodeBulkUploadView(APIView):
    serializer_class = HSCodeFileUploadSerializer

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the file to a text stream and parse it
            file_data = csv_file.read().decode('utf-8-sig').splitlines()  # Use 'utf-8-sig' to handle BOM
            reader = csv.DictReader(file_data)
            
            success_count = 0
            skip_count = 0

            for row in reader:
                hs_code = row.get('hs_code')
                description = row.get('description')

                if not hs_code or not description:
                    skip_count += 1
                    continue

                if HSCode.objects.filter(hs_code=hs_code, description=description).exists():
                    skip_count += 1
                    continue

                try:
                    HSCode.objects.create(hs_code=hs_code, description=description)
                    success_count += 1
                except Exception as e:
                    skip_count += 1
                    print(f"Failed to insert row: {row}. Error: {e}")  # Debugging

            return Response({
                "message": "CSV file data uploaded successfully!",
                "records_created": success_count,
                "records_skipped": skip_count
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
