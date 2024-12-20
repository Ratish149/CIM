from django.urls import path
from . import views
from .views import ContentItemListView, ContentItemDetailView, CategoryContentItemsView

urlpatterns = [
    path('categories/', views.InformationCategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', views.InformationCategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('faqs/', views.FAQListCreate.as_view(), name='faq-list-create'),
    path('faqs/<slug:slug>/', views.FAQRetrieveUpdateDestroy.as_view(), name='faq-detail'),
    path('information/', views.InformationListCreate.as_view(), name='information-list-create'),
    path('information/<slug:slug>/', views.InformationRetrieveUpdateDestroy.as_view(), name='information-detail'),
    path('categories/<slug:category_slug>/faqs/', views.CategoryFAQListCreate.as_view(), name='category-faq-list-create'),
    path('categories/<slug:category_slug>/information/', views.CategoryInformationListCreate.as_view(), name='category-information-list-create'),
    path('content-items/', views.ContentItemListView.as_view(), name='content-item-list'),
    path('content-items/<slug:slug>/', views.ContentItemDetailView.as_view(), name='content-item-detail'),
    path('categories/<slug:slug>/content-items/', views.CategoryContentItemsView.as_view(), name='category-content-items'),
]
