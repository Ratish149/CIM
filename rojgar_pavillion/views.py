from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from django.db import transaction
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
        Get available topics with their time slots and sessions
        """
        topics = Topic.objects.prefetch_related(
            'time_slots',
            'time_slots__training_sessions'
        )
        
        data = []
        for topic in topics:
            topic_data = {
                'id': topic.id,
                'name': topic.name,
                'time_slots': []
            }
            
            for slot in topic.time_slots.all():
                slot_data = {
                    'id': slot.id,
                    'start_time': slot.start_time,
                    'end_time': slot.end_time,
                    'max_participants': slot.max_participants,
                    'sessions': []
                }
                
                for session in slot.training_sessions.all():
                    if session.is_available():
                        slot_data['sessions'].append({
                            'id': session.id,
                            'date': session.date,
                            'available_spots': session.available_spots()
                        })
                
                if slot_data['sessions']:
                    topic_data['time_slots'].append(slot_data)
            
            if topic_data['time_slots']:
                data.append(topic_data)
        
        return Response(data)