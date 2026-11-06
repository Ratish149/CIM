from rest_framework import serializers
from .models import BDSCategory, Tags, BDSService, BDSConnect


class BDSCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BDSCategory
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class BDSServiceSerializer(serializers.ModelSerializer):
    category = BDSCategorySerializer()
    tags = TagsSerializer(many=True)

    class Meta:
        model = BDSService
        fields = '__all__'


class BDSConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BDSConnect
        fields = '__all__'
        read_only_fields = ['created_at']

    def validate(self, attrs):
        track = attrs.get('track')

        # Business track required fields
        if track == BDSConnect.TRACK_BUSINESS:
            required = {
                'name': 'Name is required.',
                'phone': 'Phone is required.',
                'business_name': 'Business name is required.',
                'district': 'District is required.',
                'sector': 'Sector is required.',
                'registered': 'Registration status is required.',
            }
            errors = {}
            for field, msg in required.items():
                if not attrs.get(field, '').strip():
                    errors[field] = msg
            if errors:
                raise serializers.ValidationError(errors)

        # Provider track required fields
        if track == BDSConnect.TRACK_PROVIDER:
            required = {
                'name': 'Contact person name is required.',
                'phone': 'Phone is required.',
                'business_name': 'Organisation name is required.',
                'district': 'District is required.',
            }
            errors = {}
            for field, msg in required.items():
                if not attrs.get(field, '').strip():
                    errors[field] = msg
            if errors:
                raise serializers.ValidationError(errors)

        return attrs
