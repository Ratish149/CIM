from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .models import Registration, Topic,TimeSlot
from .serializers import RegistrationSerializer

class RegistrationView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            registration = serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class AvailableSessionsView(generics.GenericAPIView):
    def get(self, request):
        """
        Get available topics with their time slots and remaining available spots
        """
        topics = Topic.objects.prefetch_related(
            'time_slots'  # Prefetch time slots for each topic
        )
        
        data = []
        for topic in topics:
            topic_data = {
                'id': topic.id,
                'name': topic.name,
                'time_slots': []
            }
            
            for slot in topic.time_slots.all():
                # Calculate remaining available spots
                remaining_spots = slot.max_participants - slot.current_participants
                
                slot_data = {
                    'id': slot.id,
                    'start_time': slot.start_time,
                    'end_time': slot.end_time,
                    'max_participants': slot.max_participants,
                    'current_participants': slot.current_participants,
                    'remaining_spots': remaining_spots  # Added remaining spots
                }
                
                # Only add the slot if there are remaining spots
                if remaining_spots > 0:
                    topic_data['time_slots'].append(slot_data)
            
            if topic_data['time_slots']:
                data.append(topic_data)
        
        return Response(data)