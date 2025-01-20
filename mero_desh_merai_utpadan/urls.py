from django.urls import path
from .views import (
    NatureOfIndustryCategoryListCreateView,
    NatureOfIndustrySubCategoryListCreateView,
    MeroDeshMeraiUtpadanListCreateView,
    MeroDeshMeraiUtpadanRetrieveUpdateDestroyView,
    ContactFormListCreateView,
    ApproveStatusView
)

urlpatterns = [
    path('nature-of-industry-category/', NatureOfIndustryCategoryListCreateView.as_view(), name='nature-of-industry-category-list-create'),
    path('nature-of-industry-subcategory/', NatureOfIndustrySubCategoryListCreateView.as_view(), name='nature-of-industry-subcategory-list-create'),
    path('mero-desh-merai-utpadan/', MeroDeshMeraiUtpadanListCreateView.as_view(), name='mero-desh-merai-utpadan-list-create'),
    path('mero-desh-merai-utpadan/<int:pk>/', MeroDeshMeraiUtpadanRetrieveUpdateDestroyView.as_view(), name='mero-desh-merai-utpadan-detail'),
    path('contact-form/', ContactFormListCreateView.as_view(), name='contact-form-list-create'),
    path('approve-status/<int:pk>/', ApproveStatusView.as_view(), name='approve-status'),
]
