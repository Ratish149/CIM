from django.urls import path
from .views import (
    IssueCategoryListCreateView,
    IssueSubCategoryListCreateView,
    NatureOfIndustryCategoryListCreateView,
    NatureOfIndustrySubCategoryListCreateView,
    BusinessClinicListCreateView,
)

urlpatterns = [
    path('issue-categories/', IssueCategoryListCreateView.as_view(), name='issue-category-list-create'),
    path('issue-subcategories/', IssueSubCategoryListCreateView.as_view(), name='issue-subcategory-list-create'),
    path('nature-of-industry-categories/', NatureOfIndustryCategoryListCreateView.as_view(), name='nature-of-industry-category-list-create'),
    path('nature-of-industry-subcategories/', NatureOfIndustrySubCategoryListCreateView.as_view(), name='nature-of-industry-subcategory-list-create'),
    path('business-clinics/', BusinessClinicListCreateView.as_view(), name='business-clinic-list-create'),
]
