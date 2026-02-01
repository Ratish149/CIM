# wish_and_offers/views.py

import csv

import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_filters import rest_framework as django_filters
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event

from .models import Category, HSCode, Match, Offer, Service, SubCategory, Wish
from .serializers import (
    CategorySerializer,
    CategorySubCategoryBulkUploadSerializer,
    DataConversionSerializer,
    HSCodeFileUploadSerializer,
    HSCodeSerializer,
    MatchSerializer,
    OfferSerializer,
    OfferWithWishesSerializer,
    ServiceDetailSerializer,
    ServiceSerializer,
    SubCategorySerializer,
    WishSerializer,
    WishWithOffersSerializer,
)


class WishFilterSet(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="subcategory__category__name", lookup_expr="icontains"
    )
    category_id = django_filters.CharFilter(
        field_name="subcategory__category__id", lookup_expr="exact"
    )
    subcategory = django_filters.CharFilter(
        field_name="subcategory__name", lookup_expr="icontains"
    )

    class Meta:
        model = Wish
        fields = []


class WishListCreateView(generics.ListCreateAPIView):
    serializer_class = WishSerializer
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    search_fields = ["title"]
    filterset_class = WishFilterSet

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        event_slug = self.kwargs.get("event_slug")
        if event_slug:
            queryset = Wish.objects.filter(event__slug=event_slug)
        else:
            queryset = Wish.objects.all()

        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        event_id = self.request.data.get("event_id")
        product_id = self.request.data.get("product")
        service_id = self.request.data.get("service")
        event = Event.objects.get(pk=event_id) if event_id else None

        # Retrieve the Product and Service objects
        product = HSCode.objects.get(pk=product_id) if product_id else None
        service = Service.objects.get(pk=service_id) if service_id else None

        # Capture the created wish and its matches
        wish = serializer.save(event=event, product=product, service=service, user=user)

        # Retrieve matches for the created wish
        match_objects = Match.objects.filter(wish=wish)

        # Send email to all Offer creators
        offers = Offer.objects.all()
        recipient_emails = set()
        for offer in offers:
            if offer.user and offer.user.email:
                recipient_emails.add(offer.user.email)
            elif offer.email:
                recipient_emails.add(offer.email)

        if recipient_emails:
            subject = "New Wish Added"
            context = {
                "type": "Wish",
                "title": wish.title,
                "description": wish.description,
            }
            html_message = render_to_string(
                "email_templates/new_item_notification.html", context
            )
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            send_mail(
                subject,
                plain_message,
                from_email,
                list(recipient_emails),
                html_message=html_message,
                fail_silently=True,
            )

        return Response(
            {
                "wish": WishWithOffersSerializer(wish).data,
                "matches": MatchSerializer(
                    match_objects, many=True
                ).data,  # Serialize the matches
            },
            status=status.HTTP_201_CREATED,
        )


class WishRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer

    def get(self, request, *args, **kwargs):
        wish = (
            self.get_object()
        )  # This will use the default behavior to get the wish by ID
        # Use the new serializer to get wish with offers
        wish_serializer = WishWithOffersSerializer(wish)

        return Response(wish_serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        event_id = request.data.get("event_id")
        product_id = request.data.get("product")
        service_id = request.data.get("service")

        event = Event.objects.get(pk=event_id) if event_id else instance.event
        product = HSCode.objects.get(pk=product_id) if product_id else instance.product
        service = Service.objects.get(pk=service_id) if service_id else instance.service

        # Save the updated wish and its matches
        wish = serializer.save(event=event, product=product, service=service)

        # Retrieve matches for the updated wish
        match_objects = Match.objects.filter(wish=wish)
        return Response(
            {
                "wish": WishWithOffersSerializer(wish).data,
                "matches": MatchSerializer(match_objects, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class OfferFilterSet(WishFilterSet):
    class Meta:
        model = Offer
        fields = []


class OfferListCreateView(generics.ListCreateAPIView):
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    search_fields = ["title"]
    filterset_class = OfferFilterSet

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        event_slug = self.kwargs.get("event_slug")
        if event_slug:
            queryset = Offer.objects.filter(event__slug=event_slug)
        else:
            queryset = Offer.objects.all()

        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        event_id = self.request.data.get("event_id")
        product_id = self.request.data.get("product")
        service_id = self.request.data.get("service")
        event = Event.objects.get(pk=event_id) if event_id else None

        # Retrieve the Product and Service objects
        product = HSCode.objects.get(pk=product_id) if product_id else None
        service = Service.objects.get(pk=service_id) if service_id else None

        # Capture the created offer and its matches
        offer = serializer.save(
            event=event, product=product, service=service, user=user
        )

        # Retrieve matches for the created offer
        match_objects = Match.objects.filter(offer=offer)

        # Send email to all Wish creators
        wishes = Wish.objects.all()
        recipient_emails = set()
        for wish_obj in wishes:
            if wish_obj.user and wish_obj.user.email:
                recipient_emails.add(wish_obj.user.email)
            elif wish_obj.email:
                recipient_emails.add(wish_obj.email)

        if recipient_emails:
            subject = "New Offer Added"
            context = {
                "type": "Offer",
                "title": offer.title,
                "description": offer.description,
            }
            html_message = render_to_string(
                "email_templates/new_item_notification.html", context
            )
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            send_mail(
                subject,
                plain_message,
                from_email,
                list(recipient_emails),
                html_message=html_message,
                fail_silently=True,
            )

        return Response(
            {
                "offer": OfferWithWishesSerializer(offer).data,
                "matches": MatchSerializer(
                    match_objects, many=True
                ).data,  # Serialize the matches
            },
            status=status.HTTP_201_CREATED,
        )


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve the specific offer object
        offer = (
            self.get_object()
        )  # This will use the default behavior to get the offer by ID
        # Use the new serializer to get offer with wishes
        offer_serializer = OfferWithWishesSerializer(offer)

        return Response(offer_serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        event_id = request.data.get("event_id")
        product_id = request.data.get("product")
        service_id = request.data.get("service")

        event = Event.objects.get(pk=event_id) if event_id else instance.event
        product = HSCode.objects.get(pk=product_id) if product_id else instance.product
        service = Service.objects.get(pk=service_id) if service_id else instance.service

        # Save the updated offer and its matches
        offer = serializer.save(event=event, product=product, service=service)

        # Retrieve matches for the updated offer
        match_objects = Match.objects.filter(offer=offer)
        return Response(
            {
                "offer": OfferWithWishesSerializer(offer).data,
                "matches": MatchSerializer(match_objects, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class MatchListView(generics.ListAPIView):
    queryset = Match.objects.all().order_by("id")
    serializer_class = MatchSerializer

    def get_queryset(self):
        wish_id = self.request.query_params.get("wish_id")
        offer_id = self.request.query_params.get("offer_id")

        if wish_id:
            return Match.objects.filter(wish_id=wish_id).order_by("id")
        elif offer_id:
            return Match.objects.filter(offer_id=offer_id).order_by("id")

        return super().get_queryset()  # Return all matches if no filters are applied


class ServiceFilterSet(django_filters.FilterSet):
    subcategory_id = django_filters.CharFilter(
        field_name="subcategory__id", lookup_expr="exact"
    )

    class Meta:
        model = Service
        fields = []


class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all().order_by("name")
    serializer_class = ServiceSerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = ServiceFilterSet

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ServiceDetailSerializer
        return ServiceSerializer

    def perform_create(self, serializer):
        subcategory_id = self.request.data.get(
            "subcategory_id"
        )  # Retrieve category ID from request data
        subcategory = (
            SubCategory.objects.get(pk=subcategory_id) if subcategory_id else None
        )  # Get the Category object

        # Save the service with the associated category
        serializer.save(subcategory=subcategory)  # Save the service with the category


class ServiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        service = (
            self.get_object()
        )  # This will use the default behavior to get the service by ID
        # Use the new serializer to get service with subcategory
        service_serializer = ServiceDetailSerializer(service)

        return Response(service_serializer.data)


class CategoryFilterSet(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="type", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = {
            "type": ["icontains"],
        }


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class: type[CategoryFilterSet] = CategoryFilterSet


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryFilterSet(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = SubCategory
        fields = {
            "category": ["exact"],
        }


class SubCategoryListView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all().order_by("name")
    serializer_class = SubCategorySerializer
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class: type[SubCategoryFilterSet] = SubCategoryFilterSet


class SubCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class HSCodeListView(generics.ListAPIView):
    queryset = HSCode.objects.all().order_by("hs_code")
    serializer_class = HSCodeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["hs_code", "description"]
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_queryset(self):
        queryset = HSCode.objects.all().order_by("hs_code")
        subcategory_id = self.request.query_params.get("subcategory_id", None)
        search_query = self.request.query_params.get("search", None)

        if subcategory_id:
            try:
                subcategory = SubCategory.objects.get(id=subcategory_id)
                # Only apply filtering if the category type is "Product"
                if subcategory.category.type == "Product":
                    if subcategory.reference:
                        # Split comma-separated references and create Q objects for prefix matching
                        references = [
                            ref.strip()
                            for ref in subcategory.reference.split(",")
                            if ref.strip()
                        ]
                        if references:
                            query = Q()
                            for ref in references:
                                query |= Q(hs_code__startswith=ref)
                            queryset = queryset.filter(query)
                    # If reference is empty, return all HSCodes (already the default)
                elif subcategory.category.type == "Service":
                    # HS codes are not applicable for services, return empty
                    return HSCode.objects.none()
            except SubCategory.DoesNotExist:
                pass

        if search_query:
            # If the search query contains only numbers, do a prefix search on hs_code
            if search_query.isdigit():
                queryset = queryset.filter(hs_code__startswith=search_query)
            else:
                # If the search contains text, search in both hs_code and description
                queryset = queryset.filter(
                    Q(hs_code__icontains=search_query)
                    | Q(description__icontains=search_query)
                )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # If filtering returned no results, fallback to all HS codes
        if not queryset.exists():
            queryset = HSCode.objects.all().order_by("hs_code")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HSCodeBulkUploadView(APIView):
    serializer_class = HSCodeFileUploadSerializer

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response(
                {"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode the file to a text stream and parse it
            file_data = (
                csv_file.read().decode("utf-8-sig").splitlines()
            )  # Use 'utf-8-sig' to handle BOM
            reader = csv.DictReader(file_data)

            success_count = 0
            skip_count = 0

            for row in reader:
                hs_code = row.get("hs_code")
                description = row.get("description")

                if not hs_code or not description:
                    skip_count += 1
                    continue

                if HSCode.objects.filter(
                    hs_code=hs_code, description=description
                ).exists():
                    skip_count += 1
                    continue

                try:
                    HSCode.objects.create(hs_code=hs_code, description=description)
                    success_count += 1
                except Exception as e:
                    skip_count += 1
                    print(f"Failed to insert row: {row}. Error: {e}")  # Debugging

            return Response(
                {
                    "message": "CSV file data uploaded successfully!",
                    "records_created": success_count,
                    "records_skipped": skip_count,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LatestWishAndOfferListView(generics.ListAPIView):
    def get_queryset(self):
        wishes = Wish.objects.all().order_by("-created_at")[:5]
        offers = Offer.objects.all().order_by("-created_at")[:5]
        return {"wishes": wishes, "offers": offers}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        wishes_serialized = WishWithOffersSerializer(queryset["wishes"], many=True).data
        offers_serialized = OfferWithWishesSerializer(
            queryset["offers"], many=True
        ).data
        return Response({"wishes": wishes_serialized, "offers": offers_serialized})


class CategorySubCategoryBulkUploadView(APIView):
    serializer_class = CategorySubCategoryBulkUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES.get("file")
        upload_type = serializer.validated_data.get("type", "Product")
        try:
            df = pd.read_excel(excel_file)
            # Normalize column names to lowercase to handle variations
            df.columns = [str(col).lower().strip() for col in df.columns]

            required_columns = ["category", "subcategories"]
            if not all(col in df.columns for col in required_columns):
                return Response(
                    {
                        "error": f"Missing required columns. Expected: {required_columns}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            success_count = 0
            current_category = None

            for _, row in df.iterrows():
                category_name = (
                    str(row.get("category")).strip()
                    if pd.notna(row.get("category"))
                    else None
                )
                subcategory_name = (
                    str(row.get("subcategories")).strip()
                    if pd.notna(row.get("subcategories"))
                    else None
                )
                items = (
                    str(row.get("items")).strip() if pd.notna(row.get("items")) else ""
                )
                if items in ["-", "–", "—"]:
                    items = ""

                reference = (
                    str(row.get("reference")).strip()
                    if pd.notna(row.get("reference"))
                    else ""
                )
                if reference in ["-", "–", "—"]:
                    reference = ""

                if category_name:
                    current_category, _ = Category.objects.get_or_create(
                        name=category_name, defaults={"type": upload_type}
                    )

                if current_category and subcategory_name:
                    current_subcategory, _ = SubCategory.objects.update_or_create(
                        category=current_category,
                        name=subcategory_name,
                        defaults={
                            "example_items": items,
                            "reference": reference,
                        },
                    )

                    if upload_type == "Service" and items:
                        # Split items by comma and create separate Service objects
                        service_names = [
                            s.strip() for s in items.split(",") if s.strip()
                        ]
                        for service_name in service_names:
                            Service.objects.get_or_create(
                                name=service_name, subcategory=current_subcategory
                            )

                    success_count += 1

            return Response(
                {"message": f"Successfully processed {success_count} subcategories."},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": f"Failed to process file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DataConversionView(generics.CreateAPIView):
    serializer_class = DataConversionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_type = serializer.validated_data["source_type"]
        source_id = serializer.validated_data["source_id"]

        if source_type == "wish":
            source_model = Wish
            target_model = Offer
            target_serializer = OfferSerializer
        else:
            source_model = Offer
            target_model = Wish
            target_serializer = WishSerializer

        try:
            source_obj = source_model.objects.get(id=source_id)
        except source_model.DoesNotExist:
            return Response(
                {"error": f"{source_type.capitalize()} with ID {source_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Prepare data for target
        data = {
            "full_name": source_obj.full_name,
            "user": source_obj.user,
            "designation": source_obj.designation,
            "mobile_no": source_obj.mobile_no,
            "alternate_no": source_obj.alternate_no,
            "email": source_obj.email,
            "company_name": source_obj.company_name,
            "address": source_obj.address,
            "country": source_obj.country,
            "province": source_obj.province,
            "municipality": source_obj.municipality,
            "ward": source_obj.ward,
            "company_website": source_obj.company_website,
            "image": source_obj.image,
            "title": source_obj.title,
            "description": source_obj.description,
            "event": source_obj.event,
            "product": source_obj.product,
            "service": source_obj.service,
            "subcategory": source_obj.subcategory,
            "type": source_obj.type,
            "status": "Pending",  # Reset status to Pending for the new object
        }

        with transaction.atomic():
            # Delete source first to prevent 100% match with the new target object
            source_obj.delete()
            # Create target object
            target_obj = target_model.objects.create(**data)

        return Response(
            target_serializer(target_obj).data, status=status.HTTP_201_CREATED
        )
