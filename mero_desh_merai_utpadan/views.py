from rest_framework import generics
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
from koshi_quality_standard.models import Question
from django.core.mail import EmailMessage

class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer

class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = NatureOfIndustrySubCategorySerializer
    def get_queryset(self):
        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            return NatureOfIndustrySubCategory.objects.filter(category_id=category_id)
        return NatureOfIndustrySubCategory.objects.all()

class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the instance
        instance = serializer.save()

        # Create media directory if it doesn't exist
        output_dir = "media/"
        os.makedirs(output_dir, exist_ok=True)
        output_pdf = f"{output_dir}merodeshmeraiutpadan_{instance.id}.pdf"

        # Define the path to the input PDF
        input_pdf = "media/MdMuPdf.pdf"

        # Convert English date to Nepali date
        english_date = instance.created_at
        if english_date:
            # Extract the date part from the datetime object
            english_date_only = english_date.date()
            nepali_date = nepali_datetime.date.from_datetime_date(english_date_only).strftime('%B %d, %Y')
        else:
            nepali_date = "N/A"

        # Data to populate the form fields
        field_data = {
            'ChalanNo': f"2081/82 - {instance.id}",
            'Name': instance.contact_name or "N/A",
            'CompanyName': f"{instance.contact_designation}, {instance.name_of_company} ," if (instance.contact_designation and instance.name_of_company) else "N/A",
            'Location': instance.address_street or "N/A",
            'CreatedAt': nepali_date
        }

        # Debug: Print all widget field names
        pdf = fitz.open(input_pdf)
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    print(widget.field_name)  # Print field names for verification

        # Fill the PDF
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            widgets = page.widgets()
            if widgets:
                for widget in widgets:
                    print(f"Updating widget: {widget.field_name}")
                    if widget.field_name in field_data:
                        widget.field_value = field_data[widget.field_name]
                        widget.update()

        # Save the updated PDF
        pdf.save(output_pdf)
        pdf.close()

        # Build the file URL
        file_url = request.build_absolute_uri(f"/media/merodeshmeraiutpadan_{instance.id}.pdf")

        # Save the file URL to the instance
        instance.file_url = file_url
        instance.save()

        # After PDF is generated, send email if contact_email exists
        if instance.contact_email:
            subject = 'Thank You for Participating in the "Mero Desh Merai Utpadan" Campaign'
            
            # Load the HTML template
            context = {
                'issue': instance,
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

        # Return response
        return Response({
            "message": "PDF generated successfully.",
            "file_url": file_url
        }, status=201)


class MeroDeshMeraiUtpadanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MeroDeshMeraiUtpadan.objects.all()
    serializer_class = MeroDeshMeraiUtpadanSerializer

class ContactFormListCreateView(generics.ListCreateAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

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
