from django.urls import path
from . import views

urlpatterns = [
    # Business Category URLs
    path('categories/', views.BusinessCategoryListCreateView.as_view(), name='business-category-list'),
    path('categories/<int:pk>/', views.BusinessCategoryDetailView.as_view(), name='business-category-detail'),
    
    # Business Information URLs
    path('businesses/', views.BusinessInformationListCreateView.as_view(), name='business-information-list'),
    path('businesses/<int:pk>/', views.BusinessInformationDetailView.as_view(), name='business-information-detail'),
]
