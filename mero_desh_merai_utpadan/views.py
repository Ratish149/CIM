from rest_framework import generics
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, NatureOfIndustrySubSubCategory, MeroDeshMeraiUtpadan
from .serializers import (
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    NatureOfIndustrySubSubCategorySerializer,
    MeroDeshMeraiUtpadanSerializer
)

class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustrySubCategory.objects.all()
    serializer_class = NatureOfIndustrySubCategorySerializer

class NatureOfIndustrySubSubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustrySubSubCategory.objects.all()
    serializer_class = NatureOfIndustrySubSubCategorySerializer

class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer
