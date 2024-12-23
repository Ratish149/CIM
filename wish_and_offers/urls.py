# wish_and_offers/urls.py

from django.urls import path
from .views import (
    WishListCreateView,
    WishRetrieveUpdateDestroyView,
    OfferListCreateView,
    OfferRetrieveUpdateDestroyView,
    MatchListView,
    ProductListCreateView,
    ServiceListCreateView,
    CategoryListView
)

urlpatterns = [
    # Wish URLs
    path('wishes/', WishListCreateView.as_view(), name='wish-list-create'),
    path('wishes/<int:pk>/', WishRetrieveUpdateDestroyView.as_view(), name='wish-retrieve-update-destroy'),
    
    # Offer URLs
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-retrieve-update-destroy'),
    
    # Event-specific Wish and Offer URLs
    path('events/<slug:event_slug>/wishes/', WishListCreateView.as_view(), name='wish-list-create'),
    path('events/<slug:event_slug>/wishes/<int:pk>/', WishRetrieveUpdateDestroyView.as_view(), name='wish-detail'),
    path('events/<slug:event_slug>/offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('events/<slug:event_slug>/offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-detail'),

    path('matches/', MatchListView.as_view(), name='match-list'),  # URL for listing matches

    path('wishes/<int:pk>/matched-offers/', WishRetrieveUpdateDestroyView.as_view(), name='matched-offers'),
    path('offers/<int:pk>/matched-wishes/', OfferRetrieveUpdateDestroyView.as_view(), name='matched-wishes'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),  # Updated URL for listing and creating products
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),  # Updated URL for listing and creating services
    path('categories/', CategoryListView.as_view(), name='category-list'),  # New URL for listing categories

]