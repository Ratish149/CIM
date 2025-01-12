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
    serializer_class = NatureOfIndustrySubCategorySerializer
    def get_queryset(self):
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            return NatureOfIndustrySubCategory.objects.filter(category_id=category_id)
        return NatureOfIndustrySubCategory.objects.all()

class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer

class MeroDeshMeraiUtpadanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer
