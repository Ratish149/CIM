from django.shortcuts import render
from rest_framework import generics
from .models import BDSCategory, Tags, BDSService
from .serializers import BDSCategorySerializer, TagsSerializer, BDSServiceSerializer

class BDSCategoryListCreateView(generics.ListCreateAPIView):
    queryset = BDSCategory.objects.all()
    serializer_class = BDSCategorySerializer

class TagsListCreateView(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class BDSServiceListCreateView(generics.ListCreateAPIView):
    queryset = BDSService.objects.all()
    serializer_class = BDSServiceSerializer

class BDSCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BDSCategory.objects.all()
    serializer_class = BDSCategorySerializer

class TagsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class BDSServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BDSService.objects.all()
    serializer_class = BDSServiceSerializer
