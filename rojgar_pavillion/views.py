from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Registration, Topic, TimeSlot
from .serializers import RegistrationSerializer, TopicSerializer, TimeSlotSerializer

class RegistrationView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            registration = serializer.save()
            # Increase the current participants count
            time_slot = registration.time_slot
            time_slot.current_participants += registration.total_participants
            time_slot.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class AvailableSessionsView(generics.ListAPIView):
    serializer_class = TopicSerializer
    
    def get_queryset(self):
        """
        Get active topics with available time slots
        """
        return Topic.objects.filter(
            is_active=True
        ).prefetch_related('time_slots')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_available_spots'] = True
        return context