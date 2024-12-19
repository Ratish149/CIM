from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    IssueCategorySerializer,
    IssueSubCategorySerializer,
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    IssueSerializer,
)
from .models import (
    IssueCategory,
    IssueSubCategory,
    NatureOfIndustryCategory,
    NatureOfIndustrySubCategory,
    Issue,
)

class IssueCategoryListCreateView(generics.ListCreateAPIView):
    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer

class IssueSubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = IssueSubCategory.objects.all()
    serializer_class = IssueSubCategorySerializer

class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustrySubCategory.objects.all()
    serializer_class = NatureOfIndustrySubCategorySerializer


class BusinessClinicListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
