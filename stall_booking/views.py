from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import StallBooking,SponsorBooking,ThematicSession, ThematicRegistration, GuidedTour,Invitation, SubSession, Panelist
from .serializers import StallBookingSerializer,StallBookingSmallSerializer,SponsorBookingSerializer,ThematicSessionSerializer, ThematicRegistrationSerializer, GuidedTourSerializer,InvitationSerializer, SubSessionSerializer, PanelistSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import csv
from django.core.mail import send_mail
from django.conf import settings


def export(request):
    getrec = StallBooking.objects.all()
    #csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stallbooked.csv"'

    writer = csv.writer(response)
    writer.writerow(['stallno','company','phone','email','status','stalltype','total_amount','advance_amount','remaining_amount','amount_in_words','created_at','updated_at'])

    for rec in getrec:
        writer.writerow([rec.stall_no,rec.company,rec.phone,rec.email,rec.status,rec.stall_type,rec.total_amount,rec.advance_amount,rec.remaining_amount,rec.amount_in_words,rec.created_at,rec.updated_at])
        
    return response


class StallBookingListCreateView(generics.ListCreateAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer

class StallBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer

@api_view(['POST'])
def approve_stall(request, pk):
   stall = StallBooking.objects.get(pk=pk)
   stall.status = 'Approved'
   stall.save()
   return Response({'message': 'Stall Approved', 'status': status.HTTP_200_OK})

@api_view(['POST'])
def reject_stall(request, pk):
   stall = StallBooking.objects.get(pk=pk)
   stall.status = 'Rejected'
   stall.save()
   return Response({'message': 'Stall Rejected', 'status': status.HTTP_200_OK})

@api_view(['GET'])
def get_booked_stalls(request):
   stall_type = request.GET.get('stall_type', None)
   if stall_type is not None:
      booked_stalls = StallBooking.objects.filter(status='Approved', stall_type=stall_type)
      pending_booked = StallBooking.objects.filter(status='Pending', stall_type=stall_type)
   else:
      booked_stalls = StallBooking.objects.filter(status='Approved')
      pending_booked = StallBooking.objects.filter(status='Pending')
   
   new_list = []
   for stall in booked_stalls:
      if stall.stall_no.__contains__(','):
         stall_no = stall.stall_no.split(',')
         for s in stall_no:
            new_listx = []
            new_listx.append(s)
            new_listx.append(stall.company)
            new_listx.append(stall.status)
            new_list.append(new_listx)
      else:
         new_listx = []
         new_listx.append(stall.stall_no)
         new_listx.append(stall.company)
         new_listx.append(stall.status)
         new_list.append(new_listx)

   #list to serialize
   """ new_list_json  = json.dumps(new_list) """
   
   new_list2 = []
   for stall in pending_booked:
      if stall.stall_no.__contains__(','):
         stall_no = stall.stall_no.split(',')
         for s in stall_no:
            new_list2x = []
            new_list2x.append(s)
            new_list2x.append(stall.company)
            new_list2x.append(stall.status)
            new_list2.append(new_list2x)
      else:
         new_list2x = []
         new_list2x.append(stall.stall_no)
         new_list2x.append(stall.company)
         new_list2x.append(stall.status)
         new_list2.append(new_list2x)

   #list to serialize
   """ new_list2_json  = json.dumps(new_list2) """

   serializer = StallBookingSmallSerializer(booked_stalls, many=True)
   serializer2 = StallBookingSmallSerializer(pending_booked, many=True) 
   return Response({"booked": serializer.data, "pending": serializer2.data, "stall_no_booked": new_list,"stall_no_pending": new_list2}, status=status.HTTP_200_OK)


class SponsorBookingListCreateView(generics.ListCreateAPIView):
   queryset = SponsorBooking.objects.all()
   serializer_class = SponsorBookingSerializer

class SponsorBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = SponsorBooking.objects.all()
   serializer_class = SponsorBookingSerializer

# ListCreate view for ThematicSession
class ThematicSessionListCreateView(generics.ListCreateAPIView):
    queryset = ThematicSession.objects.all().order_by('id')
    serializer_class = ThematicSessionSerializer

# RetrieveUpdateDestroy view for ThematicSession
class ThematicSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ThematicSession.objects.all()
    serializer_class = ThematicSessionSerializer

# ListCreate view for ThematicRegistration
class ThematicRegistrationListCreateView(generics.ListCreateAPIView):
    queryset = ThematicRegistration.objects.all()
    serializer_class = ThematicRegistrationSerializer

    def perform_create(self, serializer):
        sessions_data = self.request.data.get('sessions', [])
        registration = serializer.save()
        for session_id in sessions_data:
            session = ThematicSession.objects.get(id=session_id)
            registration.sessions.add(session)
        return ThematicRegistrationSerializer(registration).data
    

# RetrieveUpdateDestroy view for ThematicRegistration
class ThematicRegistrationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ThematicRegistration.objects.all()
    serializer_class = ThematicRegistrationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Update the status field directly
        if 'status' in request.data:
            instance.status = request.data['status']  # Update status directly

        # Save the updated instance
        self.perform_update(serializer)
        return Response(serializer.data)

# ListCreate view for GuidedTour
class GuidedTourListCreateView(generics.ListCreateAPIView):
    queryset = GuidedTour.objects.all()
    serializer_class = GuidedTourSerializer

    def create(self, request, *args, **kwargs):
        # Check if college is already registered
        college_name = request.data.get('college_name')
        existing_tour = GuidedTour.objects.filter(college_name=college_name).first()
        
        if existing_tour:
            return Response(
                {'error': 'This college is already registered for a guided tour'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new tour if college not registered
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send email notification
        email_subject = "New Guided Tour Registration"
        email_body = f"""
        New guided tour registration received:

        College Details:
        ---------------
        College Name: {request.data.get('college_name')}
        District: {request.data.get('district')}
        Municipality: {request.data.get('municipality')}
        Ward: {request.data.get('ward')}

        Contact Details:
        ---------------
        Contact Person: {request.data.get('contact_person_name')}
        Designation: {request.data.get('designation')}
        Phone: {request.data.get('phone')}
        Mobile: {request.data.get('mobile_no', 'Not provided')}
        Email: {request.data.get('email')}

        Tour Details:
        ------------
        Tour Date: {request.data.get('tour_date')}
        Number of Students: {request.data.get('number_of_students')}
        Student Level: {request.data.get('student_level')}

        Please keep this information for your records. If you need to make any changes to your registration, please contact +977-9862134318.

        Best regards,
        CIM 2025 Team
        """
        
        # Get college email from request data
        college_email = request.data.get('email')
        
        # Send email to both admin and college
        recipient_list = ['maanojtiwariy@gmail.com']
        if college_email:
            recipient_list.append(college_email)
            
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

# RetrieveUpdateDestroy view for GuidedTour
class GuidedTourRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GuidedTour.objects.all()
    serializer_class = GuidedTourSerializer

class InvitationListCreateView(generics.ListCreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

@api_view(['POST'])
def approve_thematic_registration(request, pk):
    try:
        registration = ThematicRegistration.objects.get(pk=pk)
        
        # Update status to Approved
        registration.status = 'Approved'
        registration.save()

        # Only send emails if status is Approved
        if registration.status == 'Approved':
            # Get hotel email from the request data
            hotel_email = request.data.get('hotel_email')
            participant_email = registration.email

            # Prepare email content using an HTML template
            email_subject = "Guest Information"
            context = {
                'name': registration.name,
                'address': registration.address,
                'contact': registration.contact,
                'email': registration.email,
                'check_in_date': registration.check_in_date,
                'check_out_date': registration.check_out_date,
                'hotel': registration.hotel,
                'hotel_accomodation': registration.hotel_accomodation,
            }

            email_body = render_to_string('email_template/guest_information.html', context)

            # Send email to hotel only if hotel_email is provided
            if hotel_email:
                send_mail(
                    email_subject,
                    settings.DEFAULT_FROM_EMAIL,
                    [hotel_email],
                    fail_silently=False,
                    html_message=email_body
                )
            
            # Send email to participant
            send_mail(
                email_subject,
                settings.DEFAULT_FROM_EMAIL,
                [participant_email],
                fail_silently=False,
                html_message=email_body
            )
            
            message = 'Registration Approved and emails sent'
            if not hotel_email:
                message = 'Registration Approved and email sent to participant only'
            
            return Response({'message': message, 'status': status.HTTP_200_OK})
        
        return Response({'message': 'Registration status updated', 'status': status.HTTP_200_OK})
    except ThematicRegistration.DoesNotExist:
        return Response({'error': 'ThematicRegistration not found'}, status=status.HTTP_404_NOT_FOUND)

# ListCreate view for SubSession
class SubSessionListCreateView(generics.ListCreateAPIView):
    queryset = SubSession.objects.all()
    serializer_class = SubSessionSerializer

# RetrieveUpdateDestroy view for SubSession
class SubSessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubSession.objects.all()
    serializer_class = SubSessionSerializer

# ListCreate view for Panelist
class PanelistListCreateView(generics.ListCreateAPIView):
    queryset = Panelist.objects.all()
    serializer_class = PanelistSerializer

# RetrieveUpdateDestroy view for Panelist
class PanelistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Panelist.objects.all()
    serializer_class = PanelistSerializer