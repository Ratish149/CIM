from rest_framework import serializers

from accounts.serializers import UserSerializer, UserSmallSerializer
from wish_and_offers.serializers import OfferSmallSerializer, WishSmallSerializer

from .models import AgendaItem, Attendee, Event, Sponsor, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ["id", "name", "logo", "website"]


class AgendaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaItem
        fields = ["id", "time", "title", "description", "speaker", "date"]


class AttendeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = ["id", "user", "registration_date"]


class AttendeeSmallSerializer(serializers.ModelSerializer):
    user = UserSmallSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = ["id", "user"]


class EventListSerializer(serializers.ModelSerializer):
    organizer = UserSmallSerializer(read_only=True)
    attendees_count = serializers.SerializerMethodField()
    attendees = AttendeeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    sponsor = SponsorSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "tags",
            "start_date",
            "end_date",
            "location",
            "organizer",
            "attendees_count",
            "thumbnail",
            "slug",
            "sponsor",
            "attendees",
            "contact_person",
            "contact_number",
        ]

    def get_attendees_count(self, obj):
        # Count both Wish and Offer details associated with this event
        wish_count = obj.wishes.filter(status="Pending").count()
        offer_count = obj.offers.filter(status="Pending").count()
        return wish_count + offer_count


class EventDetailSerializer(serializers.ModelSerializer):
    organizer = UserSmallSerializer(read_only=True)
    attendees = AttendeeSmallSerializer(many=True, read_only=True)
    wishes = WishSmallSerializer(many=True, read_only=True)
    offers = OfferSmallSerializer(many=True, read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)
    agenda_items = AgendaItemSerializer(many=True, read_only=True)
    attendees_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "organizer",
            "attendees_count",
            "attendees",
            "sponsors",
            "agenda_items",
            "event_file",
            "created_at",
            "updated_at",
            "thumbnail",
            "wishes",
            "offers",
            "slug",
            "tags",
            "contact_person",
            "contact_number",
        ]

    def get_attendees_count(self, obj):
        # Count both Wish and Offer details associated with this event
        wish_count = obj.wishes.filter(status="Pending").count()
        offer_count = obj.offers.filter(status="Pending").count()
        return wish_count + offer_count


class EventCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )
    organizer = UserSmallSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "organizer",
            "thumbnail",
            "slug",
            "tags",
            "contact_person",
            "contact_number",
            "status",
            "is_featured",
            "is_popular",
        ]
