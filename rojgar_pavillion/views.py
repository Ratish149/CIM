from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Registration, Topic, TimeSlot
from .serializers import RegistrationSerializer, TopicSerializer, TimeSlotSerializer, RegistrationDetailSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse  # Import reverse to build URLs
from django.http import HttpRequest  # Import HttpRequest if needed

def send_confirmation_email(request: HttpRequest, registration, status):
        try:

            # Prepare the context for the email template
            print(registration.qr_code)
            full_qr_code_link = request.build_absolute_uri(registration.qr_code.url)  # Generate full link for qr_code
            print(full_qr_code_link)
            context = {
                'registration': registration.id,
                'registration_date': registration.created_at.strftime('%B %d, %Y'),
                'number_of_participants': registration.total_participants,
                'total_amount': registration.total_price,
                'full_name': registration.first_name + " " + registration.last_name,
                'email': registration.email or 'N/A',
                'mobile_number': registration.mobile_number or 'N/A',
                'qualification': registration.qualification or 'N/A',
                'gender': registration.gender or 'N/A',
                'age': registration.age or 'N/A',
                'address': registration.address or 'N/A',
                'status': status,
                'qr_code': full_qr_code_link,  # Use the full link in the context
                'topic': registration.time_slot.topic.name,
                'date': registration.time_slot.date.strftime('%B %d, %Y'),
                'time_slot': registration.time_slot.start_time.strftime('%I:%M %p'),
                'flight_no': registration.flight_no or 'N/A',
                'arrival_date': registration.arrival_date or 'N/A',
                'arrival_time': registration.arrival_time or 'N/A',
                'return_flight_no': registration.return_flight_no or 'N/A',
                'return_flight_time': registration.return_flight_time or 'N/A',
                'departure_time': registration.departure_time or 'N/A',
            }

            # HTML email content using the registration_confirmation.html template
            html_message = render_to_string('emails/registration_confirmation.html', context)
            

            # Modify recipient list based on status
            recipient_list = [registration.email]
            if status == 'Pending':
                recipient_list.append('ajit.chapagain@gmail.com')  # Append additional email for pending status

            # Send email with both HTML and plain text versions
            send_mail(
                subject=f'Registration {status} - Birat Expo 2025',
                message=f'Your registration has been {status}. Please check your email for details.',  # Fallback message for plain text
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Email sent successfully to {registration.email}")
        except Exception as e:
            print(f"Failed to send email to {registration.email}: {str(e)}")

class RegistrationView(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegistrationSerializer
        return RegistrationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            registration = serializer.save()
            # Increase the current participants count
            time_slot = registration.time_slot
            time_slot.current_participants += registration.total_participants
            time_slot.save()

            # Send confirmation email with status 'pending'
            send_confirmation_email(request, registration, status='Pending')

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )



class RegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationDetailSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        status = instance.status        
        send_confirmation_email(self.request, instance, status)

class AvailableSessionsView(generics.ListAPIView):
    serializer_class = TopicSerializer
    
    def get_queryset(self):
        """
        Get active topics with available time slots
        """
        return Topic.objects.filter(
            is_active=True
        ).prefetch_related('time_slot_instances')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_available_spots'] = True
        return context
    
class TimeSlotByDateView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')  # Get the date from query parameters
        topic = self.request.query_params.get('topic')
        top = Topic.objects.get(id=topic)
        if date:
            return TimeSlot.objects.filter(date=date,topic=top).order_by('start_time')  # Filter time slots by the provided date
        return TimeSlot.objects.none() 

class UpdateAttendanceView(generics.UpdateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationDetailSerializer

    def update(self, request, *args, **kwargs):
        registration = self.get_object()
        registration.is_attended = True  # Update the is_attended field
        registration.save()  # Save the changes

        return Response(
            {'status': 'Attendance updated successfully'},
            status=status.HTTP_200_OK
        ) 