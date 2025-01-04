from django.urls import path
from .views import (
    NatureOfIndustryCategoryListCreateView,
    NatureOfIndustrySubCategoryListCreateView,
    IssueListCreateView,
    IssueDetailView,
)

urlpatterns = [
    path('nature-of-industry-categories/', 
         NatureOfIndustryCategoryListCreateView.as_view(), 
         name='nature-of-industry-category-list-create'),
    
    path('nature-of-industry-subcategories/', 
         NatureOfIndustrySubCategoryListCreateView.as_view(), 
         name='nature-of-industry-subcategory-list-create'),
    
    path('issues/', 
         IssueListCreateView.as_view(), 
         name='issue-list-create'),
    
    path('issues/<int:pk>/', 
         IssueDetailView.as_view(), 
         name='issue-detail'),
]
