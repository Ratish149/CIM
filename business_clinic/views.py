from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    IssueCategorySerializer,
    IssueSubCategorySerializer,
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    NatureOfIndustrySubSubCategorySerializer,
    Business_ClinicSerializer,
)
from .models import (
    IssueCategory,
    IssueSubCategory,
    NatureOfIndustryCategory,
    NatureOfIndustrySubCategory,
    NatureOfIndustrySubSubCategory,
    Business_Clinic,
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

class NatureOfIndustrySubSubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustrySubSubCategory.objects.all()
    serializer_class = NatureOfIndustrySubSubCategorySerializer

class BusinessClinicListCreateView(generics.ListCreateAPIView):
    queryset = Business_Clinic.objects.all()
    serializer_class = Business_ClinicSerializer
