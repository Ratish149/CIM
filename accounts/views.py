from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, File, Organization
from .serializers import (
    FileSerializer,
    OrganizationSerializer,
    RegisterSerializer,
    UserSerializer,
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        refresh["user_id"] = user.id
        refresh["first_name"] = user.first_name
        refresh["last_name"] = user.last_name
        refresh["email"] = user.email
        refresh["phone_number"] = user.phone_number
        refresh["address"] = user.address

        is_institute_verified = (
            getattr(user, "institute", None).is_verified
            if getattr(user, "institute", None)
            else False
        )
        refresh["is_institute_verified"] = is_institute_verified

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                return Response(
                    {
                        "detail": "Invalid password",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except CustomUser.DoesNotExist:
            return Response(
                {
                    "detail": f"User with this email {email} does not exist",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        refresh = RefreshToken.for_user(user)
        refresh["user_id"] = user.id
        refresh["first_name"] = user.first_name
        refresh["last_name"] = user.last_name
        refresh["email"] = user.email
        refresh["phone_number"] = user.phone_number
        refresh["address"] = user.address
        refresh["is_institute"] = user.has_institute
        institute = getattr(user, "institute", None)
        refresh["institute"] = institute.id if institute else None

        is_institute_verified = institute.is_verified if institute else False
        refresh["is_institute_verified"] = is_institute_verified

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class FileListCreateView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    # permission_classes = [permissions.IsAuthenticated]


class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
