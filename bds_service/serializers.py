from rest_framework import serializers
from .models import BDSCategory, Tags, BDSService

class BDSCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BDSCategory
        fields = '__all__'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class BDSServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BDSService
        fields = '__all__'
