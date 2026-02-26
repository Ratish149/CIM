# wish_and_offers/urls.py

from django.urls import path

from .views import (
    CategoryListView,
    CategoryRetrieveUpdateDestroyView,
    CategorySubCategoryBulkUploadView,
    DataConversionView,
    HSCodeBulkUploadView,
    HSCodeListView,
    IncreaseOfferViewCountView,
    IncreaseWishViewCountView,
    LatestWishAndOfferListView,
    MatchListView,
    OfferListCreateView,
    OfferRetrieveUpdateDestroyView,
    ServiceListCreateView,
    ServiceRetrieveUpdateDestroyView,
    SubCategoryListView,
    SubCategoryRetrieveUpdateDestroyView,
    WishAndOfferCombinedListView,
    WishListCreateView,
    WishRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Wish URLs
    path("wishes/", WishListCreateView.as_view(), name="wish-list-create"),
    path(
        "wishes/<int:pk>/",
        WishRetrieveUpdateDestroyView.as_view(),
        name="wish-retrieve-update-destroy",
    ),
    # Offer URLs
    path("offers/", OfferListCreateView.as_view(), name="offer-list-create"),
    path(
        "offers/<int:pk>/",
        OfferRetrieveUpdateDestroyView.as_view(),
        name="offer-retrieve-update-destroy",
    ),
    path(
        "wish-offers/",
        LatestWishAndOfferListView.as_view(),
        name="latest-wish-and-offer-list",
    ),
    path(
        "combined/",
        WishAndOfferCombinedListView.as_view(),
        name="wish-offer-combined-list",
    ),
    # Event-specific Wish and Offer URLs
    path(
        "events/<slug:event_slug>/wishes/",
        WishListCreateView.as_view(),
        name="wish-list-create",
    ),
    path(
        "events/<slug:event_slug>/wishes/<int:pk>/",
        WishRetrieveUpdateDestroyView.as_view(),
        name="wish-detail",
    ),
    path(
        "events/<slug:event_slug>/offers/",
        OfferListCreateView.as_view(),
        name="offer-list-create",
    ),
    path(
        "events/<slug:event_slug>/offers/<int:pk>/",
        OfferRetrieveUpdateDestroyView.as_view(),
        name="offer-detail",
    ),
    path(
        "matches/", MatchListView.as_view(), name="match-list"
    ),  # URL for listing matches
    path("services/", ServiceListCreateView.as_view(), name="service-list-create"),
    path(
        "services/<int:pk>/",
        ServiceRetrieveUpdateDestroyView.as_view(),
        name="service-detail",
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/bulk-upload/",
        CategorySubCategoryBulkUploadView.as_view(),
        name="category-bulk-upload",
    ),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-retrieve-update-destroy",
    ),
    path("sub-categories/", SubCategoryListView.as_view(), name="sub-category-list"),
    path(
        "sub-categories/<int:pk>/",
        SubCategoryRetrieveUpdateDestroyView.as_view(),
        name="sub-category-retrieve-update-destroy",
    ),
    path("hs-codes/", HSCodeListView.as_view(), name="hs-code-list"),
    path("hs-codes/upload/", HSCodeBulkUploadView.as_view(), name="hs-code-upload"),
    path("convert-data/", DataConversionView.as_view(), name="data-conversion"),
    # View Count Increment URLs
    path(
        "wishes/<int:pk>/view/",
        IncreaseWishViewCountView.as_view(),
        name="increase-wish-view-count",
    ),
    path(
        "offers/<int:pk>/view/",
        IncreaseOfferViewCountView.as_view(),
        name="increase-offer-view-count",
    ),
]
