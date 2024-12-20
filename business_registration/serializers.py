from rest_framework import serializers
from .models import InformationCategory, FAQ, Information, ContentItem

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'slug', 'created_at', 'updated_at']

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = ['id', 'title', 'description', 'slug', 'created_at', 'updated_at']

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['id', 'title', 'slug', 'content', 'external_url', 'is_featured', 'content_type', 'category']


class InformationCategorySerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, read_only=True)
    information = InformationSerializer(many=True, read_only=True)
    content_items = ContentItemSerializer(many=True, read_only=True)

    class Meta:
        model = InformationCategory
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at', 'faqs', 'information', 'content_items']
