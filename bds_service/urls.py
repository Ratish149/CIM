from django.urls import path
from .views import BDSCategoryListCreateView, TagsListCreateView, BDSServiceListCreateView

urlpatterns = [
    path('categories/', BDSCategoryListCreateView.as_view(), name='bds-category-list-create'),
    path('tags/', TagsListCreateView.as_view(), name='tags-list-create'),
    path('services/', BDSServiceListCreateView.as_view(), name='bds-service-list-create'),
]
