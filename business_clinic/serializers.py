from rest_framework import serializers
from .models import IssueCategory,IssueSubCategory,NatureOfIndustryCategory,NatureOfIndustrySubCategory,Business_Clinic

class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = '__all__'

class IssueSubCategorySerializer(serializers.ModelSerializer):
    category=IssueCategorySerializer(read_only=True)
    class Meta:
        model = IssueSubCategory
        fields = '__all__'

class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = '__all__'

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    category=NatureOfIndustryCategorySerializer(read_only=True)
    class Meta:
        model = NatureOfIndustrySubCategory
        fields = '__all__'

class Business_ClinicSerializer(serializers.ModelSerializer):
    nature_of_industry_sub_category = NatureOfIndustrySubCategorySerializer(read_only=True)
    issue_sub_category=IssueSubCategorySerializer(read_only=True)
    class Meta:
        model = Business_Clinic
        fields = '__all__'