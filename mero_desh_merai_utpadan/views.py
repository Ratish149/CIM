from rest_framework import generics
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan
from .serializers import (
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    MeroDeshMeraiUtpadanSerializer
)

class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustrySubCategory.objects.all()
    serializer_class = NatureOfIndustrySubCategorySerializer

class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer

class MeroDeshMeraiUtpadanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer
