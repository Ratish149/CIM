from rest_framework import serializers

from accounts.serializers import UserSerializer, UserSmallSerializer
from wish_and_offers.serializers import OfferSmallSerializer, WishSmallSerializer

from .models import (
    AgendaItem,
    Attendee,
    Event,
    EventImage,
    EventOrganizer,
    Sponsor,
    Tag,
)


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


class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = ["id", "name", "logo", "email", "phone", "address"]


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ["id", "image"]


class EventImageCreateSerializer(serializers.ModelSerializer):
    # We define this to handle multiple files in the input
    images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = EventImage
        fields = ["id", "event", "images"]  # 'event' is needed to link the images

    def create(self, validated_data):
        images_data = validated_data.pop("images")
        event = validated_data.pop("event")
        image_instances = []

        for image_data in images_data:
            instance = EventImage.objects.create(event=event, image=image_data)
            image_instances.append(instance)

        return image_instances  # Note: This returns a list, so the View needs to handle the response


class EventListSerializer(serializers.ModelSerializer):
    event_organizer = EventOrganizerSerializer(read_only=True)
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
            "event_organizer",
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
    event_organizer = EventOrganizerSerializer(read_only=True)
    attendees = AttendeeSmallSerializer(many=True, read_only=True)
    wishes = WishSmallSerializer(many=True, read_only=True)
    offers = OfferSmallSerializer(many=True, read_only=True)
    sponsors = SponsorSerializer(many=True, read_only=True)
    agenda_items = AgendaItemSerializer(many=True, read_only=True)
    attendees_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    images = EventImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "event_organizer",
            "attendees_count",
            "attendees",
            "sponsors",
            "agenda_items",
            "event_file",
            "images",
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
    event_organizer = serializers.PrimaryKeyRelatedField(
        queryset=EventOrganizer.objects.all(), required=False
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "event_organizer",
            "thumbnail",
            "slug",
            "tags",
            "event_file",
            "order",
            "contact_person",
            "contact_number",
            "status",
            "is_featured",
            "is_popular",
        ]
