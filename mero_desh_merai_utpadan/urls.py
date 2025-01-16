from django.urls import path
from .views import (
    NatureOfIndustryCategoryListCreateView,
    NatureOfIndustrySubCategoryListCreateView,
    MeroDeshMeraiUtpadanListCreateView,
    MeroDeshMeraiUtpadanRetrieveUpdateDestroyView,
    ContactFormListCreateView,
)

urlpatterns = [
    path('nature-of-industry-category/', NatureOfIndustryCategoryListCreateView.as_view(), name='nature-of-industry-category-list-create'),
    path('nature-of-industry-sub-category/', NatureOfIndustrySubCategoryListCreateView.as_view(), name='nature-of-industry-sub-category-list-create'),
    path('mero-desh-merai-utpadan/', MeroDeshMeraiUtpadanListCreateView.as_view(), name='mero-desh-merai-utpadan-list-create'),
    path('mero-desh-merai-utpadan/<int:pk>/', MeroDeshMeraiUtpadanRetrieveUpdateDestroyView.as_view(), name='merodeshmeraiutpadan-detail'),
    path('contact-form-submit/', ContactFormListCreateView.as_view(), name='contact-form-submit'),
]
