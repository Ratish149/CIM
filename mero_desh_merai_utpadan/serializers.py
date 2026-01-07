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
    company_logo = serializers.FileField(required=False, allow_null=True)
    nature_of_industry_category = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustryCategory.objects.all()
    )
    nature_of_industry_sub_category = serializers.PrimaryKeyRelatedField(
        queryset=NatureOfIndustrySubCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    nature_of_industry_sub_category_detail = NatureOfIndustrySubCategorySerializer(
        source="nature_of_industry_sub_category", read_only=True
    )

    class Meta:
        model = MeroDeshMeraiUtpadan
        fields = "__all__"

    def create(self, validated_data):
        company_logo = validated_data.pop("company_logo", None)
        name_of_company = validated_data.get("name_of_company")
        mero_desh_merai_utpadan = MeroDeshMeraiUtpadan.objects.create(**validated_data)
        if company_logo:
            logo = CompanyLogo.objects.create(name=name_of_company, logo=company_logo)
            mero_desh_merai_utpadan.company_logo = logo
            mero_desh_merai_utpadan.save()
        return mero_desh_merai_utpadan

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.company_logo:
            representation["company_logo"] = CompanyLogoListSerializer(
                instance.company_logo
            ).data
        return representation


class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"


class CompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLogo
        fields = "__all__"


class CompanyLogoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLogo
        fields = ["id", "name", "slug", "logo"]
