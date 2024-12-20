# wish_and_offers/urls.py

from django.urls import path
from .views import (
    WishListCreateView,
    WishRetrieveUpdateDestroyView,
    OfferListCreateView,
    OfferRetrieveUpdateDestroyView
)

urlpatterns = [
    # Wish URLs
    path('wishes/', WishListCreateView.as_view(), name='wish-list-create'),
    path('wishes/<int:pk>/', WishRetrieveUpdateDestroyView.as_view(), name='wish-retrieve-update-destroy'),
    
    # Offer URLs
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-retrieve-update-destroy'),
    
    # Event-specific Wish and Offer URLs
    path('events/<int:event_id>/wishes/', WishListCreateView.as_view(), name='event-wish-list-create'),
    path('events/<int:event_id>/offers/', OfferListCreateView.as_view(), name='event-offer-list-create'),
]