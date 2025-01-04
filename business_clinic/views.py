from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    IssueSerializer,
)
from .models import (
    NatureOfIndustryCategory,
    NatureOfIndustrySubCategory,
    Issue,
)

class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustrySubCategory.objects.all()
    serializer_class = NatureOfIndustrySubCategorySerializer

class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class IssueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
