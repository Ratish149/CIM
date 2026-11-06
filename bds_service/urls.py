from django.urls import path

from .views import (
    BDSCategoryDetailView,
    BDSCategoryListCreateView,
    BDSConnectCreateView,
    BDSConnectDetailView,
    BDSConnectListView,
    BDSServiceDetailView,
    BDSServiceListCreateView,
    TagsDetailView,
    TagsListCreateView,
)

urlpatterns = [
    # BDSCategory
    path("categories/", BDSCategoryListCreateView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/", BDSCategoryDetailView.as_view(), name="category-detail"
    ),
    # Tags
    path("tags/", TagsListCreateView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagsDetailView.as_view(), name="tag-detail"),
    # BDSService
    path("services/", BDSServiceListCreateView.as_view(), name="service-list"),
    path("services/<int:pk>/", BDSServiceDetailView.as_view(), name="service-detail"),
    # BDSConnect
    path("connect/", BDSConnectListView.as_view(), name="bds-connect-list"),
    path(
        "connect/register/", BDSConnectCreateView.as_view(), name="bds-connect-create"
    ),
    path(
        "connect/<int:pk>/", BDSConnectDetailView.as_view(), name="bds-connect-detail"
    ),
]
