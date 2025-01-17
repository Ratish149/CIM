from django.urls import path
from .views import (
    BDSCategoryListCreateView, BDSCategoryDetailView,
    TagsListCreateView, TagsDetailView,
    BDSServiceListCreateView, BDSServiceDetailView
)

urlpatterns = [
    # BDSCategory URLs
    path('categories/', BDSCategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', BDSCategoryDetailView.as_view(), name='category-detail'),
    
    # Tags URLs
    path('tags/', TagsListCreateView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagsDetailView.as_view(), name='tag-detail'),
    
    # BDSService URLs
    path('services/', BDSServiceListCreateView.as_view(), name='service-list'),
    path('services/<int:pk>/', BDSServiceDetailView.as_view(), name='service-detail'),
]
