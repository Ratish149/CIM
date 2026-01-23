from django.urls import path

from .views import (
    AgendaItemListCreateView,
    AgendaItemRetrieveUpdateDestroyView,
    AttendeeListCreateView,
    AttendeeRetrieveDestroyView,
    EventImageListCreateView,
    EventImageRetreveUpdateDeleteView,
    EventListCreateView,
    EventOrganizerListCreateView,
    EventOrganizerRetreveUpdateDeleteView,
    EventRetrieveUpdateDestroyView,
    GetFeaturedEvents,
    GetPopularEvents,
    PastEventListView,
    SponsorListCreateView,
    SponsorRetrieveUpdateDestroyView,
    TagListCreateView,
    TagRetreveUpdateDeleteView,
)

urlpatterns = [
    path(
        "event-tags/",
        TagListCreateView.as_view(),
        name="event-organizer-list-create",
    ),
    path(
        "event-tags/<int:id>/",
        TagRetreveUpdateDeleteView.as_view(),
        name="event-detail",
    ),
    path(
        "event-organizers/",
        EventOrganizerListCreateView.as_view(),
        name="event-organizer-list-create",
    ),
    path(
        "event-organizers/<int:id>/",
        EventOrganizerRetreveUpdateDeleteView.as_view(),
        name="event-detail",
    ),
    path("event-images/", EventImageListCreateView.as_view(), name="event-list-create"),
    path(
        "event-images/<int:id>/",
        EventImageRetreveUpdateDeleteView.as_view(),
        name="event-detail",
    ),
    path("events/", EventListCreateView.as_view(), name="event-list-create"),
    path("past-events/", PastEventListView.as_view(), name="past-event-list"),
    path(
        "events/<str:slug>/",
        EventRetrieveUpdateDestroyView.as_view(),
        name="event-detail",
    ),
    path(
        "events/<int:event_id>/attendees/",
        AttendeeListCreateView.as_view(),
        name="attendee-list-create",
    ),
    path(
        "events/<int:event_id>/attendees/<int:pk>/",
        AttendeeRetrieveDestroyView.as_view(),
        name="attendee-retrieve-destroy",
    ),
    path(
        "events/<int:event_id>/sponsors/",
        SponsorListCreateView.as_view(),
        name="sponsor-list-create",
    ),
    path(
        "events/<int:event_id>/sponsors/<int:pk>/",
        SponsorRetrieveUpdateDestroyView.as_view(),
        name="sponsor-retrieve-update-destroy",
    ),
    path(
        "events/<int:event_id>/agenda/",
        AgendaItemListCreateView.as_view(),
        name="agenda-item-list-create",
    ),
    path(
        "events/<int:event_id>/agenda/<int:pk>/",
        AgendaItemRetrieveUpdateDestroyView.as_view(),
        name="agenda-item-retrieve-update-destroy",
    ),
    path("popular-events/", GetPopularEvents.as_view(), name="popular-events"),
    path(
        "featured-events/",
        GetFeaturedEvents.as_view(),
        name="featured-published-events",
    ),
]
