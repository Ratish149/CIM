from django.urls import path
from .views import (
    EventListCreateView,
    EventRetrieveUpdateDestroyView,
    AttendeeListCreateView,
    AttendeeRetrieveDestroyView,
    SponsorListCreateView,
    SponsorRetrieveUpdateDestroyView,
    AgendaItemListCreateView,
    AgendaItemRetrieveUpdateDestroyView,

    GetPopularEvents,
    GetFeaturedEvents
)

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list-create'),

    path('events/<slug:slug>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('events/<int:event_id>/attendees/', AttendeeListCreateView.as_view(), name='attendee-list-create'),
    path('events/<int:event_id>/attendees/<int:pk>/', AttendeeRetrieveDestroyView.as_view(), name='attendee-retrieve-destroy'),
    path('events/<int:event_id>/sponsors/', SponsorListCreateView.as_view(), name='sponsor-list-create'),
    path('events/<int:event_id>/sponsors/<int:pk>/', SponsorRetrieveUpdateDestroyView.as_view(), name='sponsor-retrieve-update-destroy'),
    path('events/<int:event_id>/agenda/', AgendaItemListCreateView.as_view(), name='agenda-item-list-create'),
    path('events/<int:event_id>/agenda/<int:pk>/', AgendaItemRetrieveUpdateDestroyView.as_view(), name='agenda-item-retrieve-update-destroy'),
    path('popular-events/', GetPopularEvents.as_view(), name='popular-events'),
    path('featured-events/', GetFeaturedEvents.as_view(), name='featured-published-events'),
]