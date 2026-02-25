from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from jobbriz_institute.serializers import GraduateRosterListSerializer

from .filters import GraduateRosterFilter
from .models import GraduateRoster, Institute
from .serializers import GraduateRosterSerializer, InstituteSerializer


class InstituteTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, institute, timestamp):
        return str(institute.pk) + str(timestamp) + str(institute.is_verified)


institute_token_generator = InstituteTokenGenerator()


def send_verification_email(institute):
    uid = urlsafe_base64_encode(force_bytes(institute.pk))
    token = institute_token_generator.make_token(institute)
    domain = "https://www.biratbazaar.com"
    verification_url = f"{domain}/institutes/verify/{uid}/{token}/"

    subject = "Please verify your Institute Email"
    context = {
        "institute_name": institute.institute_name,
        "verification_url": verification_url,
    }
    html_content = render_to_string("emails/verify_institute_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, to=[institute.email])
    email.attach_alternative(html_content, "text/html")
    email.send()


class InstituteListCreateView(generics.ListCreateAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        institute = serializer.save(user=self.request.user)
        user = self.request.user
        user.has_institute = True
        user.save()

        # Send verification email
        send_verification_email(institute)


class InstituteVerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            institute = Institute.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Institute.DoesNotExist):
            institute = None

        if institute is not None and institute_token_generator.check_token(
            institute, token
        ):
            institute.is_verified = True
            institute.save()
            return Response(
                {"message": "Email verified successfully!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendInstituteVerifyEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        institute = getattr(request.user, "institute", None)
        if not institute:
            return Response(
                {"error": "User is not associated with any institute."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if institute.is_verified:
            return Response(
                {"message": "Institute is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_verification_email(institute)
        return Response(
            {"message": "Verification email resent successfully!"},
            status=status.HTTP_200_OK,
        )


class InstituteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return getattr(self.request.user, "institute", None)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response(None)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GraduateRosterListCreateView(generics.ListCreateAPIView):
    queryset = GraduateRoster.objects.all().order_by("-created_at")
    serializer_class = GraduateRosterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = GraduateRosterFilter
    search_fields = ["name", "specialization_key_skills", "subject_trade_stream"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return GraduateRosterSerializer
        return GraduateRosterListSerializer

    def perform_create(self, serializer):
        roster_type = self.request.data.get("roster_type")
        if roster_type == "Individual":
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class MyGraduateRosterListView(generics.ListAPIView):
    queryset = GraduateRoster.objects.all()
    serializer_class = GraduateRosterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GraduateRosterFilter

    def get_queryset(self):
        user = self.request.user
        return GraduateRoster.objects.filter(user=user)


class GraduateRosterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GraduateRoster.objects.all()
    serializer_class = GraduateRosterSerializer


class InstituteGraduateRosterListView(generics.ListAPIView):
    queryset = GraduateRoster.objects.all()
    serializer_class = GraduateRosterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GraduateRosterFilter

    def get_queryset(self):
        institute = getattr(self.request.user, "institute", None)
        return GraduateRoster.objects.filter(institute=institute)
