from django.urls import path
from .views import (
    UserListCreateView, UserRetrieveUpdateDestroyView, UserRegistrationView,
    FileListCreateView, FileRetrieveUpdateDestroyView,
    OrganizationListCreateView, OrganizationRetrieveUpdateDestroyView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-retrieve-update-destroy'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='organization-retrieve-update-destroy'),
]