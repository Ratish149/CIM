# wish_and_offers/serializers.py

from django.conf import settings
from rest_framework import serializers

from .models import Category, HSCode, Match, Offer, Service, SubCategory, Wish


class HSCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSCode
        fields = ["id", "hs_code", "description"]


class SubCategorySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySmallSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "image", "type", "subcategories"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
            "example_items",
            "reference",
            "image",
            "category",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "image", "subcategory"]


class ServiceDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySmallSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ["id", "name", "image", "subcategory"]


class WishSerializer(serializers.ModelSerializer):
    product = HSCodeSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Wish
        fields = [
            "id",
            "full_name",
            "offer",
            "user",
            "designation",
            "mobile_no",
            "alternate_no",
            "email",
            "company_name",
            "address",
            "country",
            "province",
            "municipality",
            "ward",
            "company_website",
            "image",
            "title",
            "description",
            "event",
            "subcategory",
            "product",
            "service",
            "status",
            "type",
            "match_percentage",
            "created_at",
            "updated_at",
        ]


class OfferSerializer(serializers.ModelSerializer):
    product = HSCodeSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "wish",
            "full_name",
            "designation",
            "mobile_no",
            "alternate_no",
            "email",
            "company_name",
            "address",
            "country",
            "province",
            "municipality",
            "ward",
            "company_website",
            "subcategory",
            "image",
            "title",
            "description",
            "event",
            "product",
            "service",
            "status",
            "type",
            "match_percentage",
            "created_at",
            "updated_at",
        ]


class WishWithOffersSerializer(serializers.ModelSerializer):
    offers = serializers.SerializerMethodField()

    class Meta:
        model = Wish
        fields = [
            "id",
            "full_name",
            "designation",
            "mobile_no",
            "alternate_no",
            "email",
            "company_name",
            "address",
            "country",
            "province",
            "municipality",
            "ward",
            "company_website",
            "image",
            "title",
            "description",
            "event",
            "product",
            "service",
            "status",
            "type",
            "match_percentage",
            "created_at",
            "updated_at",
            "offers",
        ]

    def get_offers(self, obj):
        # Use prefetched matches if available, otherwise filter
        if hasattr(obj, "matches"):
            matches = obj.matches.all()
        else:
            matches = Match.objects.filter(wish=obj).select_related("offer")

        offers = [match.offer for match in matches]
        return OfferSerializer(offers, many=True).data


class OfferWithWishesSerializer(serializers.ModelSerializer):
    wishes = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "full_name",
            "designation",
            "mobile_no",
            "alternate_no",
            "email",
            "company_name",
            "address",
            "country",
            "province",
            "municipality",
            "ward",
            "company_website",
            "image",
            "title",
            "description",
            "event",
            "product",
            "service",
            "status",
            "type",
            "match_percentage",
            "created_at",
            "updated_at",
            "wishes",
        ]

    def get_wishes(self, obj):
        # Use prefetched matches if available, otherwise filter
        if hasattr(obj, "matches"):
            matches = obj.matches.all()
        else:
            matches = Match.objects.filter(offer=obj).select_related("wish")

        wishes = [match.wish for match in matches]
        return WishSerializer(wishes, many=True).data


class MatchSerializer(serializers.ModelSerializer):
    wish = WishWithOffersSerializer(read_only=True)
    offer = OfferWithWishesSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ["id", "wish", "offer", "created_at", "updated_at"]


class WishSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = [
            "id",
            "title",
            "description",
            "product",
            "service",
            "status",
            "type",
            "created_at",
            "updated_at",
        ]


class OfferSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "description",
            "product",
            "service",
            "status",
            "type",
            "created_at",
            "updated_at",
        ]


class CategorySubCategoryBulkUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    type = serializers.ChoiceField(choices=Category.TYPE, default="Product")

    def validate_file(self, value):
        if not value.name.endswith((".xlsx", ".xls")):
            raise serializers.ValidationError(
                "Only Excel files (.xlsx, .xls) are allowed"
            )
        return value


class HSCodeFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith(".csv"):
            raise serializers.ValidationError("Only CSV files are allowed")
        return value


class DataConversionSerializer(serializers.Serializer):
    TYPE_CHOICES = [
        ("wish", "Wish"),
        ("offer", "Offer"),
    ]
    source_type = serializers.ChoiceField(choices=TYPE_CHOICES)
    source_id = serializers.IntegerField()
    target_type = serializers.ChoiceField(choices=TYPE_CHOICES)

    def validate(self, data):
        if data["source_type"] == data["target_type"]:
            raise serializers.ValidationError(
                "Source and target types must be different."
            )
        return data


class CombinedWishOfferSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    model_type = serializers.CharField()
    full_name = serializers.CharField()
    designation = serializers.CharField()
    mobile_no = serializers.CharField()
    alternate_no = serializers.CharField()
    email = serializers.EmailField()
    company_name = serializers.CharField()
    address = serializers.CharField()
    country = serializers.CharField()
    province = serializers.CharField()
    municipality = serializers.CharField()
    ward = serializers.CharField()
    company_website = serializers.CharField()
    image = serializers.SerializerMethodField()
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    type = serializers.CharField()
    match_percentage = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_image(self, obj):
        image = obj.get("image")
        if not image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + str(image))
        return settings.MEDIA_URL + str(image)

    # Nested fields
    product = HSCodeSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    # Foreign key IDs mapped from union result
    subcategory = serializers.IntegerField(source="subcategory_id", allow_null=True)
    event = serializers.IntegerField(source="event_id", allow_null=True)
    user = serializers.IntegerField(source="user_id", allow_null=True)
    offer = serializers.IntegerField(source="offer_id", allow_null=True, required=False)
    wish = serializers.IntegerField(source="wish_id", allow_null=True, required=False)
