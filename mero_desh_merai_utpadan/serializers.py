from rest_framework import serializers
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan,ContactForm
from django.template.loader import render_to_string
import os


class NatureOfIndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfIndustryCategory
        fields = '__all__'  # or specify fields as needed

class NatureOfIndustrySubCategorySerializer(serializers.ModelSerializer):
    category = NatureOfIndustryCategorySerializer(read_only=True)
    class Meta:
        model = NatureOfIndustrySubCategory
        fields = '__all__'  # or specify fields as needed


class MeroDeshMeraiUtpadanSerializer(serializers.ModelSerializer):
    nature_of_industry_category = serializers.PrimaryKeyRelatedField(queryset=NatureOfIndustryCategory.objects.all())
    nature_of_industry_sub_category = serializers.PrimaryKeyRelatedField(queryset=NatureOfIndustrySubCategory.objects.all())
    nature_of_industry_sub_category_detail = NatureOfIndustrySubCategorySerializer(source='nature_of_industry_sub_category', read_only=True)
    
    class Meta:
        model = MeroDeshMeraiUtpadan
        fields = '__all__'

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'

