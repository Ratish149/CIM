from rest_framework import serializers
from .models import IssueCategory,IssueSubCategory,NatureOfIndustryCategory,NatureOfIndustrySubCategory,NatureOfIndustrySubSubCategory,Business_Clinic

class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = '__all__'

class IssueSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueSubCategory
        fields = '__all__'

class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = '__all__'

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustrySubCategory
        fields = '__all__'

class NatureOfIndustrySubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustrySubSubCategory
        fields = '__all__'

class Business_ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business_Clinic
        fields = '__all__'