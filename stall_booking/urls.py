from django.urls import path
from . import views

urlpatterns = [
   path('stall/',views.StallBookingListCreateView.as_view(),name='stall-list-create'),
   path('export/',views.export,name='export'),
   path('stall/<int:pk>/',views.StallBookingRetrieveUpdateDestroyView.as_view(),name='stall-retrieve-update-destroy'),
   path("get-booked-stalls/", views.get_booked_stalls, name="get booked stalls"),
   path('approve-stall/<int:pk>/',views.approve_stall,name='approve stall'),
   path('reject-stall/<int:pk>/',views.reject_stall,name='reject stall'),
   path('sponsor/',views.SponsorBookingListCreateView.as_view(),name='sponsor-list-create'),
   path('sponsor/<int:pk>/',views.SponsorBookingRetrieveUpdateDestroyView.as_view(),name='sponsor-retrieve-update-destroy'),
   path('thematic-sessions/', views.ThematicSessionListCreateView.as_view(), name='thematic-session-list-create'),
   path('thematic-sessions/<int:pk>/', views.ThematicSessionRetrieveUpdateDestroyView.as_view(), name='thematic-session-detail'),

   # ThematicRegistration URLs
   path('thematic-registrations/', views.ThematicRegistrationListCreateView.as_view(), name='thematic-registration-list-create'),
   path('thematic-registrations/<int:pk>/', views.ThematicRegistrationRetrieveUpdateDestroyView.as_view(), name='thematic-registration-detail'),

   # GuidedTour URLs
   path('guided-tours/', views.GuidedTourListCreateView.as_view(), name='guided-tour-list-create'),
   path('guided-tours/<int:pk>/', views.GuidedTourRetrieveUpdateDestroyView.as_view(), name='guided-tour-detail'),
   path('rsvp/', views.InvitationListCreateView.as_view(), name='invitation-list-create'),
   path('approve-thematic-registration/<int:pk>/', views.approve_thematic_registration, name='approve_thematic_registration'),

   # URLs for SubSession
   path('subsessions/', views.SubSessionListCreateView.as_view(), name='subsession-list-create'),
   path('subsessions/<int:pk>/', views.SubSessionRetrieveUpdateDestroyView.as_view(), name='subsession-detail'),

   # URLs for Panelist
   path('panelists/', views.PanelistListCreateView.as_view(), name='panelist-list-create'),
   path('panelists/<int:pk>/', views.PanelistRetrieveUpdateDestroyView.as_view(), name='panelist-detail'),
]
