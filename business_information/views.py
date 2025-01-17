from django.shortcuts import render
from rest_framework import generics
from .models import BusinessCategory, BusinessInformation
from .serializers import BusinessCategorySerializer, BusinessInformationSerializer

class BusinessCategoryListCreateView(generics.ListCreateAPIView):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer

class BusinessInformationListCreateView(generics.ListCreateAPIView):
    queryset = BusinessInformation.objects.all()
    serializer_class = BusinessInformationSerializer

class BusinessCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer

class BusinessInformationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessInformation.objects.all()
    serializer_class = BusinessInformationSerializer
