from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    CompanyLogo,
    ContactForm,
    MeroDeshMeraiUtpadan,
    NatureOfIndustryCategory,
    NatureOfIndustrySubCategory,
)
from .serializers import (
    CompanyLogoSerializer,
    ContactFormSerializer,
    MeroDeshMeraiUtpadanSerializer,
    NatureOfIndustryCategorySerializer,
    NatureOfIndustrySubCategorySerializer,
)
from .utils import process_mdmu_approval


class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 100


class NatureOfIndustryCategoryListCreateView(generics.ListCreateAPIView):
    queryset = NatureOfIndustryCategory.objects.all()
    serializer_class = NatureOfIndustryCategorySerializer
    pagination_class = CustomPagination


class NatureOfIndustrySubCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = NatureOfIndustrySubCategorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        category_id = self.request.query_params.get("category", None)
        if category_id is not None:
            return NatureOfIndustrySubCategory.objects.filter(category_id=category_id)
        return NatureOfIndustrySubCategory.objects.all()


class MeroDeshMeraiUtpadanListCreateView(generics.ListCreateAPIView):
    serializer_class = MeroDeshMeraiUtpadanSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = MeroDeshMeraiUtpadan.objects.all()

        # Search functionality
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(name_of_company__icontains=search)
                | models.Q(contact_name__icontains=search)
                | models.Q(contact_email__icontains=search)
            )

        # Industry Category filters
        category = self.request.query_params.get("category")
        subcategory = self.request.query_params.get("subcategory")

        category_query = models.Q()

        if category:
            category_list = category.split(",")
            category_query &= models.Q(
                nature_of_industry_category__name__icontains=category_list
            )

        if subcategory:
            subcategory_list = subcategory.split(",")
            category_query &= models.Q(
                nature_of_industry_sub_category__name__icontains=subcategory_list
            )

        if category_query:
            queryset = queryset.filter(category_query)

        # Location filters
        province = self.request.query_params.get("province")
        district = self.request.query_params.get("district")
        municipality = self.request.query_params.get("municipality")

        if province:
            queryset = queryset.filter(address_province__iexact=province)
        if district:
            queryset = queryset.filter(address_district__iexact=district)
        if municipality:
            queryset = queryset.filter(address_municipality__iexact=municipality)

        # Industry size filter
        industry_size = self.request.query_params.get("industry_size")
        if industry_size:
            queryset = queryset.filter(industry_size=industry_size)

        # Market and raw material filters
        product_market = self.request.query_params.get("market_type")
        if product_market:
            queryset = queryset.filter(product_market=product_market)

        raw_material = self.request.query_params.get("raw_material")
        if raw_material:
            queryset = queryset.filter(raw_material=raw_material)

        # Boolean filters
        member_of_cim = self.request.query_params.get("member_of_cim")
        if member_of_cim is not None:
            queryset = queryset.filter(member_of_cim=member_of_cim.lower() == "true")

        interested_in_logo = self.request.query_params.get("interested_in_logo")
        if interested_in_logo is not None:
            queryset = queryset.filter(
                interested_in_logo=interested_in_logo.lower() == "true"
            )

        # Date range filter
        date_filter = self.request.query_params.get("date_filter")
        if date_filter:
            if date_filter == "last_24_hours":
                date_threshold = timezone.now() - timezone.timedelta(days=1)
            elif date_filter == "last_week":
                date_threshold = timezone.now() - timezone.timedelta(days=7)
            elif date_filter == "last_month":
                date_threshold = timezone.now() - timezone.timedelta(days=30)
            elif date_filter == "last_3_months":
                date_threshold = timezone.now() - timezone.timedelta(days=90)
            elif date_filter == "last_year":
                date_threshold = timezone.now() - timezone.timedelta(days=365)

            queryset = queryset.filter(created_at__gte=date_threshold)

        # Custom date range
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])

        return queryset.order_by("-created_at").distinct()

    def list(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        queryset = self.get_queryset()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=user)

        # Automatically approve and send email
        success, error_message = process_mdmu_approval(instance, new_status="Approved")

        if not success:
            # We still return 201 because the instance was created, but we might want to log the error
            return Response(
                {
                    "message": "Registration successful, but there was an error processing approval/email.",
                    "error": error_message,
                    "data": serializer.data,
                },
                status=201,
            )

        return Response(
            {
                "message": "Registration successful and automatically approved.",
                "data": serializer.data,
            },
            status=201,
        )


class MeroDeshMeraiUtpadanRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
):
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
            "name": serializer.validated_data["name"],
            "email": serializer.validated_data["email"],
            "phone_number": serializer.validated_data["phone_number"],
            "subject": serializer.validated_data["subject"],
            "message": serializer.validated_data["message"],
        }

        # Render the HTML template
        html_message = render_to_string(
            "email_template/contact_form_email.html", context
        )

        # Send email to admin
        subject = f"New Contact Form Submission for Mero Desh Merai Utpadan: {serializer.validated_data['subject']}"
        from_email = settings.DEFAULT_FROM_EMAIL

        # Update recipient_list to include the specified email
        recipient_list = ["biratexpo2024@gmail.com"]  # Updated recipient list

        # Send both HTML and plain text versions
        send_mail(
            subject=subject,
            message=strip_tags(html_message),  # Plain text version
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,  # HTML version
        )

        return Response({"message": "Contact form submitted successfully."}, status=201)


class ApproveStatusView(APIView):
    def patch(self, request, pk):
        instance = get_object_or_404(MeroDeshMeraiUtpadan, pk=pk)
        new_status = request.query_params.get("status")

        if not new_status:
            return Response(
                {"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in ["Pending", "Approved", "Rejected"]:
            return Response(
                {"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST
            )

        success, error_message = process_mdmu_approval(instance, new_status=new_status)

        if success:
            return Response(
                {
                    "message": f"Status updated to {new_status} successfully",
                    "file_url": instance.file_url if new_status == "Approved" else None,
                }
            )
        else:
            return Response(
                {"error": f"Error processing status update: {error_message}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CompanyLogoListView(generics.ListCreateAPIView):
    queryset = CompanyLogo.objects.all()
    serializer_class = CompanyLogoSerializer


class CompanyLogoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyLogo.objects.all()
    serializer_class = CompanyLogoSerializer
    lookup_field = "slug"
