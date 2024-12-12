from rest_framework import serializers
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, NatureOfIndustrySubSubCategory, MeroDeshMeraiUtpadan

class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = '__all__'  # or specify fields as needed

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustrySubCategory
        fields = '__all__'  # or specify fields as needed

class NatureOfIndustrySubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustrySubSubCategory
        fields = '__all__'  # or specify fields as needed

class MeroDeshMeraiUtpadanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeroDeshMeraiUtpadan
        fields = '__all__'  # or specify fields as needed
