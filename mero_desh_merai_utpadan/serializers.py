from rest_framework import serializers

from .models import (
    CompanyLogo,
    ContactForm,
    MeroDeshMeraiUtpadan,
    NatureOfIndustryCategory,
    NatureOfIndustrySubCategory,
)


class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = "__all__"  # or specify fields as needed


class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    category = NatureOfIndustryCategorySerializer(read_only=True)

    class Meta:
        model = NatureOfIndustrySubCategory
        fields = "__all__"  # or specify fields as needed


class MeroDeshMeraiUtpadanSerializer(serializers.ModelSerializer):
    nature_of_industry_category = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustryCategory.objects.all()
    )
    nature_of_industry_sub_category = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustrySubCategory.objects.all()
    )
    nature_of_industry_sub_category_detail = NatureOfIndustrySubCategorySerializer(
        source="nature_of_industry_sub_category", read_only=True
    )

    class Meta:
        model = MeroDeshMeraiUtpadan
        fields = "__all__"


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"


class CompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLogo
        fields = "__all__"
