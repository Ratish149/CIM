from django.urls import path

from . import views

urlpatterns = [
    path(
        "institutes/",
        views.InstituteListCreateView.as_view(),
        name="institute-list-create",
    ),
    path(
        "institutes/detail/",
        views.InstituteRetrieveUpdateDestroyView.as_view(),
        name="institute-retrieve-update-destroy",
    ),
    path(
        "graduates/",
        views.GraduateRosterListCreateView.as_view(),
        name="graduate-roster-list-create",
    ),
    path(
        "graduates/<int:pk>/",
        views.GraduateRosterRetrieveUpdateDestroyView.as_view(),
        name="graduate-roster-retrieve-update-destroy",
    ),
    path(
        "institute-graduates/",
        views.InstituteGraduateRosterListView.as_view(),
        name="institute-graduate-roster-list-create",
    ),
    path(
        "institutes/verify/<str:uidb64>/<str:token>/",
        views.InstituteVerifyEmailView.as_view(),
        name="institute-verify-email",
    ),
    path(
        "institutes/resend-verification/",
        views.ResendInstituteVerifyEmailView.as_view(),
        name="institute-resend-verification",
    ),
]
