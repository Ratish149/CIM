# wish_and_offers/serializers.py

from rest_framework import serializers
from .models import Wish, Offer, Product, Service, Category, Match
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'hs_code', 'description', 'image', 'category']

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'image', 'category']

class WishSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Wish
        fields = [
            'id', 'full_name', 'designation', 'mobile_no', 'alternate_no',
            'email', 'company_name', 'address', 'country', 'province',
            'municipality', 'ward', 'company_website', 'image',
            'title', 'event', 'product', 'service', 'status', 'wish_type','match_percentage',
            'created_at', 'updated_at'
        ]

class OfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'full_name', 'designation', 'mobile_no', 'alternate_no',
            'email', 'company_name', 'address', 'country', 'province',
            'municipality', 'ward', 'company_website', 'image',
            'title', 'event', 'product', 'service', 'status', 'offer_type','match_percentage',
            'created_at', 'updated_at'
        ]

class WishWithOffersSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField()

    class Meta:
        model = Wish
        fields = ['id', 'full_name', 'designation', 'mobile_no', 'alternate_no',
                  'email', 'company_name', 'address', 'country', 'province',
                  'municipality', 'ward', 'company_website', 'image',
                  'title', 'event', 'product', 'service', 'status', 
                  'wish_type', 'match_percentage', 'created_at', 'updated_at', 'offers']

    def get_offers(self, obj):
        # Retrieve offers related to this wish through the Match model
        matches = Match.objects.filter(wish=obj)
        offers = [match.offer for match in matches]
        return OfferSerializer(offers, many=True).data

class OfferWithWishesSerializer(serializers.ModelSerializer):
    wishes = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'full_name', 'designation', 'mobile_no', 'alternate_no',
                  'email', 'company_name', 'address', 'country', 'province',
                  'municipality', 'ward', 'company_website', 'image',
                  'title', 'event', 'product', 'service', 'status', 
                  'offer_type', 'match_percentage', 'created_at', 'updated_at', 'wishes']

    def get_wishes(self, obj):
        # Retrieve wishes related to this offer through the Match model
        matches = Match.objects.filter(offer=obj)
        wishes = [match.wish for match in matches]
        return WishSerializer(wishes, many=True).data

class MatchSerializer(serializers.ModelSerializer):
    wish = WishWithOffersSerializer(read_only=True)
    offer = OfferWithWishesSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'wish', 'offer', 'created_at', 'updated_at']

class WishSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ['id', 'title','product', 'service', 'status', 'wish_type', 'created_at', 'updated_at']

class OfferSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'title','product', 'service', 'status', 'offer_type', 'created_at', 'updated_at']