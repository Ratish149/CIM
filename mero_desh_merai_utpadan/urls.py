from django.urls import path

from .views import (
    ApproveStatusView,
    CompanyLogoListView,
    CompanyLogoRetrieveUpdateDestroyView,
    ContactFormListCreateView,
    MeroDeshMeraiUtpadanListCreateView,
    MeroDeshMeraiUtpadanRetrieveUpdateDestroyView,
    NatureOfIndustryCategoryListCreateView,
    NatureOfIndustrySubCategoryListCreateView,
)

urlpatterns = [
    path(
        "nature-of-industry-category/",
        NatureOfIndustryCategoryListCreateView.as_view(),
        name="nature-of-industry-category-list-create",
    ),
    path(
        "nature-of-industry-sub-category/",
        NatureOfIndustrySubCategoryListCreateView.as_view(),
        name="nature-of-industry-sub-category-list-create",
    ),
    path(
        "mero-desh-merai-utpadan/",
        MeroDeshMeraiUtpadanListCreateView.as_view(),
        name="mero-desh-merai-utpadan-list-create",
    ),
    path(
        "mero-desh-merai-utpadan/<int:pk>/",
        MeroDeshMeraiUtpadanRetrieveUpdateDestroyView.as_view(),
        name="merodeshmeraiutpadan-detail",
    ),
    path(
        "contact-form-submit/",
        ContactFormListCreateView.as_view(),
        name="contact-form-submit",
    ),
    path("<int:pk>/status/", ApproveStatusView.as_view(), name="approve-status"),
    path("company-logo/", CompanyLogoListView.as_view(), name="company-logo-list"),
    path(
        "company-logo/<slug:slug>/",
        CompanyLogoRetrieveUpdateDestroyView.as_view(),
        name="company-logo-detail",
    ),
]
