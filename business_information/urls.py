from django.urls import path
from .views import BusinessCategoryListCreateView, BusinessInformationListCreateView

urlpatterns = [
    path('business-categories/', BusinessCategoryListCreateView.as_view(), name='business-category-list-create'),
    path('business-information/', BusinessInformationListCreateView.as_view(), name='business-information-list-create'),
]
