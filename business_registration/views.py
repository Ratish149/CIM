from django.shortcuts import render
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import InformationCategory, FAQ, Information, ContentItem
from .serializers import InformationCategorySerializer, FAQSerializer, InformationSerializer, ContentItemSerializer

# Create your views here.

class InformationCategoryListCreate(generics.ListCreateAPIView):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class InformationCategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    lookup_field = 'slug'

class FAQListCreate(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['question', 'created_at']
    ordering = ['question']

class FAQRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    lookup_field = 'slug'

class InformationListCreate(generics.ListCreateAPIView):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['title', 'created_at']
    ordering = ['title']

class InformationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
    lookup_field = 'slug'

class CategoryFAQListCreate(generics.ListCreateAPIView):
    serializer_class = FAQSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['question', 'created_at']
    ordering = ['question']

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return FAQ.objects.filter(category__slug=category_slug)

    def perform_create(self, serializer):
        category = InformationCategory.objects.get(slug=self.kwargs['category_slug'])
        serializer.save(category=category)

class CategoryInformationListCreate(generics.ListCreateAPIView):
    serializer_class = InformationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'created_at']
    ordering = ['title']

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Information.objects.filter(category__slug=category_slug)

    def perform_create(self, serializer):
        category = InformationCategory.objects.get(slug=self.kwargs['category_slug'])
        serializer.save(category=category)

class ContentItemListView(generics.ListCreateAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer

class ContentItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    lookup_field = 'slug'

class CategoryContentItemsView(generics.RetrieveAPIView):
    queryset = InformationCategory.objects.all()
    serializer_class = InformationCategorySerializer
    lookup_field = 'slug'
