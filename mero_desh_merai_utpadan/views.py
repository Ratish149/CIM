from rest_framework import generics, status
from django.db import models
from .models import NatureOfIndustryCategory, NatureOfIndustrySubCategory, MeroDeshMeraiUtpadan,ContactForm
from .serializers import (
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
    MeroDeshMeraiUtpadanSerializer,
    ContactFormSerializer
)
import fitz
import os
from rest_framework.response import Response
import nepali_datetime
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer
    pagination_class = CustomPagination

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = NatureOfIndustrySubCategorySerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            return NatureOfIndustrySubCategory.objects.filter(category_id=category_id)
        return NatureOfIndustrySubCategory.objects.all()

class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    serializer_class = MeroDeshMeraiUtpadanSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = MeroDeshMeraiUtpadan.objects.all()
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name_of_company__icontains=search) |
                models.Q(contact_name__icontains=search) |
                models.Q(contact_email__icontains=search)
            )
        
        # Industry Category filters
        category = self.request.query_params.get('category')
        subcategory = self.request.query_params.get('subcategory')
        
        category_query = models.Q()
        
        if category:
            category_list = category.split(',')
            category_query &= models.Q(nature_of_industry_category__name__icontains=category_list)
        
        if subcategory:
            subcategory_list = subcategory.split(',')
            category_query &= models.Q(nature_of_industry_sub_category__name__icontains=subcategory_list)
        
        if category_query:
            queryset = queryset.filter(category_query)
        
        # Location filters
        province = self.request.query_params.get('province')
        district = self.request.query_params.get('district')
        municipality = self.request.query_params.get('municipality')
        
        if province:
            queryset = queryset.filter(address_province__iexact=province)
        if district:
            queryset = queryset.filter(address_district__iexact=district)
        if municipality:
            queryset = queryset.filter(address_municipality__iexact=municipality)
        
        # Industry size filter
        industry_size = self.request.query_params.get('industry_size')
        if industry_size:
            queryset = queryset.filter(industry_size=industry_size)
        
        # Market and raw material filters
        product_market = self.request.query_params.get('market_type')
        if product_market:
            queryset = queryset.filter(product_market=product_market)
            
        raw_material = self.request.query_params.get('raw_material')
        if raw_material:
            queryset = queryset.filter(raw_material=raw_material)
        
        # Boolean filters
        member_of_cim = self.request.query_params.get('member_of_cim')
        if member_of_cim is not None:
            queryset = queryset.filter(member_of_cim=member_of_cim.lower() == 'true')
            
        interested_in_logo = self.request.query_params.get('interested_in_logo')
        if interested_in_logo is not None:
            queryset = queryset.filter(interested_in_logo=interested_in_logo.lower() == 'true')
        
        # Date range filter
        date_filter = self.request.query_params.get('date_filter')
        if date_filter:
            if date_filter == 'last_24_hours':
                date_threshold = timezone.now() - timezone.timedelta(days=1)
            elif date_filter == 'last_week':
                date_threshold = timezone.now() - timezone.timedelta(days=7)
            elif date_filter == 'last_month':
                date_threshold = timezone.now() - timezone.timedelta(days=30)
            elif date_filter == 'last_3_months':
                date_threshold = timezone.now() - timezone.timedelta(days=90)
            elif date_filter == 'last_year':
                date_threshold = timezone.now() - timezone.timedelta(days=365)
            
            queryset = queryset.filter(created_at__gte=date_threshold)
        
        # Custom date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])
        
        return queryset.order_by('-created_at').distinct()

    def list(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        queryset = self.get_queryset()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        return Response({
            "message": "Registration successful.",
            "data": serializer.data
        }, status=201)

class MeroDeshMeraiUtpadanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer

class ContactFormListCreateView(generics.ListCreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Prepare context for email template
        context = {
            'name': serializer.validated_data['name'],
            'email': serializer.validated_data['email'],
            'phone_number': serializer.validated_data['phone_number'],
            'subject': serializer.validated_data['subject'],
            'message': serializer.validated_data['message']
        }

        # Render the HTML template
        html_message = render_to_string(
            'email_template/contact_form_email.html',
            context
        )

        # Send email to admin
        subject = f"New Contact Form Submission: {serializer.validated_data['subject']}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.DEFAULT_FROM_EMAIL]
        
        # Send both HTML and plain text versions
        send_mail(
            subject=subject,
            message=strip_tags(html_message),  # Plain text version
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message  # HTML version
        )

        return Response({"message": "Contact form submitted successfully."}, status=201)

class ApproveStatusView(APIView):
    def patch(self, request, pk):
        instance = get_object_or_404(MeroDeshMeraiUtpadan, pk=pk)
        new_status = request.query_params.get('status')
        
        if not new_status:
            return Response(
                {"error": "Status is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if new_status not in ['Pending', 'Approved', 'Rejected']:
            return Response(
                {"error": "Invalid status value"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if new_status == 'Approved':
                # Create pdf directory inside media if it doesn't exist
                output_dir = "media/pdf/mdmu/"
                os.makedirs(output_dir, exist_ok=True)
                output_pdf = f"{output_dir}merodeshmeraiutpadan_{instance.id}.pdf"

                # Define the path to the input PDF
                input_pdf = "media/mdmu_final.pdf"

                # Convert English date to Nepali date
                english_date = instance.created_at
                if english_date:
                    english_date_only = english_date.date()
                    nepali_date = nepali_datetime.date.from_datetime_date(english_date_only).strftime('%B %d, %Y')
                else:
                    nepali_date = "N/A"

                # Data to populate the form fields
                field_data = {
                    'ChalanNo': f"2081/82 - {instance.id}",
                    'CompanyName': instance.name_of_company or "N/A",
                    'Location': instance.address_street or "N/A",
                    'CreatedAt': nepali_date
                }

                # Fill the PDF
                pdf = fitz.open(input_pdf)
                for page_num in range(len(pdf)):
                    page = pdf[page_num]
                    widgets = page.widgets()
                    if widgets:
                        for widget in widgets:
                            if widget.field_name in field_data:
                                widget.field_value = field_data[widget.field_name]
                                widget.update()

                # Save the updated PDF
                pdf.save(output_pdf)
                pdf.close()

                # Build the file URL
                file_url = f"/media/pdf/mdmu/merodeshmeraiutpadan_{instance.id}.pdf"
                instance.file_url = file_url

                # Send email if contact_email exists
                if instance.contact_email:
                    subject = 'Thank You for Participating in the "Mero Desh Merai Utpadan" Campaign'
                    
                    # Load the HTML template
                    context = {
                        'issue': instance,
                        'name': instance.contact_name,
                        'logo_url': os.path.join(settings.STATIC_ROOT, 'logo', 'mdmu-logo.png'),
                    }
                    html_message = render_to_string('email_template/mdmu_email_template.html', context)

                    # Create email message
                    email = EmailMessage(
                        subject=subject,
                        body=html_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[instance.contact_email],
                    )
                    
                    # Attach the generated PDF
                    with open(output_pdf, 'rb') as pdf_file:
                        email.attach(f'merodeshmeraiutpadan_{instance.id}.pdf', pdf_file.read(), 'application/pdf')

                    # Attach the logo
                    logo_path = os.path.join(settings.STATIC_ROOT, 'logo', 'mdmu-logo.png')
                    with open(logo_path, 'rb') as logo_file:
                        email.attach('mdmu-logo.png', logo_file.read(), 'image/png')

                    email.content_subtype = 'html'
                    email.send(fail_silently=False)

            elif new_status == 'Rejected' and instance.contact_email:
                # Send rejection email
                subject = 'Update on Your "Mero Desh Merai Utpadan" Campaign Application'
                
                context = {
                    'name': instance.contact_name,
                    'company_name': instance.name_of_company,
                }
                html_message = render_to_string('email_template/mdmu_rejection_email.html', context)

                email = EmailMessage(
                    subject=subject,
                    body=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[instance.contact_email],
                )

                email.content_subtype = 'html'
                email.send(fail_silently=False)

            # Update the status
            instance.status = new_status
            instance.save()

            return Response({
                "message": f"Status updated to {new_status} successfully",
                "file_url": instance.file_url if new_status == 'Approved' else None
            })

        except Exception as e:
            return Response(
                {"error": f"Error processing status update: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
