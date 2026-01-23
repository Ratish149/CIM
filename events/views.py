from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import EventFilter
from .models import (
    AgendaItem,
    Attendee,
    Event,
    EventImage,
    EventOrganizer,
    Sponsor,
    Tag,
)
from .serializers import (
    AgendaItemSerializer,
    AttendeeSerializer,
    EventCreateSerializer,
    EventDetailSerializer,
    EventImageCreateSerializer,
    EventImageSerializer,
    EventListSerializer,
    EventOrganizerSerializer,
    SponsorSerializer,
    TagSerializer,
)


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetreveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "id"


class EventOrganizerListCreateView(generics.ListCreateAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer


class EventOrganizerRetreveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventOrganizer.objects.all()
    serializer_class = EventOrganizerSerializer
    lookup_field = "id"


class EventImageListCreateView(generics.ListCreateAPIView):
    queryset = EventImage.objects.all()
    serializer_class = EventImageCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        image_instances = serializer.save()

        output_serializer = EventImageSerializer(image_instances, many=True)

        return Response(
            {
                "message": f"Successfully uploaded {len(image_instances)} images.",
                "data": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventImageCreateSerializer
        return EventImageSerializer


class EventImageRetreveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventImage.objects.all()
    serializer_class = EventImageSerializer
    lookup_field = "id"


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"  # Allow client to override page size
    max_page_size = 100  # Maximum


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(status="Published").order_by("start_date")
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        return EventListSerializer

    def perform_create(self, serializer):
        serializer.save()


class PastEventListView(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(
            status="Published", end_date__lt=timezone.now().date()
        ).order_by("start_date")


class GetFeaturedEvents(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(status="Published", is_featured=True).order_by(
            "order"
        )


class GetPopularEvents(generics.ListAPIView):
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(status="Published", is_popular=True).order_by(
            "order"
        )


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = "slug"


class AttendeeListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs["event_id"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_id"])
        serializer.save(user=self.request.user, event=event)


class AttendeeRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event_id=self.kwargs["event_id"])


class SponsorListCreateView(generics.ListCreateAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Sponsor.objects.filter(event_id=self.kwargs["event_id"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_id"])
        serializer.save(event=event)


class SponsorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Sponsor.objects.filter(event_id=self.kwargs["event_id"])


class AgendaItemListCreateView(generics.ListCreateAPIView):
    serializer_class = AgendaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgendaItem.objects.filter(event_id=self.kwargs["event_id"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_id"])
        serializer.save(event=event)


class AgendaItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgendaItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return AgendaItem.objects.filter(event_id=self.kwargs["event_id"])
