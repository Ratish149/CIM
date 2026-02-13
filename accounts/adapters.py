from typing import Any, Dict

from allauth.account.utils import user_email, user_field, user_username
from allauth.headless.adapter import DefaultHeadlessAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for Google OAuth authentication.
    Uses Django's default User model with no modifications.
    """

    pass

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.
        This is called for new users only, after the user has been created.
        """

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        name = data.get("name")
        username = data.get("username", email)

        user = sociallogin.user

        # Set user fields
        user_username(user, username)
        user_email(user, email or "")
        name_parts = (name or "").partition(" ")
        user_field(user, "first_name", first_name or name_parts[0])
        user_field(user, "last_name", last_name or name_parts[2])

        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Save the user and add to appropriate group.
        This is called after populate_user for new users.
        """
        user = super().save_user(request, sociallogin, form)

        return user


class CustomHeadlessAdapter(DefaultHeadlessAdapter):
    """
    Custom headless adapter that returns JWT tokens safely for authenticated users.
    """

    def serialize_user(self, user) -> Dict[str, Any]:
        ret = {
            "display": user.first_name + " " + user.last_name,
        }

        # Safe JWT creation
        try:
            refresh = RefreshToken.for_user(user)
            # Add custom claims
            refresh["email"] = user.email
            refresh["username"] = user.username
            refresh["first_name"] = user.first_name
            refresh["last_name"] = user.last_name

            # Return tokens
            ret["access_token"] = str(refresh.access_token)
            ret["refresh_token"] = str(refresh)

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Error creating JWT token for user {user.id}: {str(e)}")
            # Return basic user info without tokens as fallback
            # The frontend should handle this case
            ret["error"] = "Token creation failed"

        print("CustomHeadlessAdapter serialize_user", ret)

        return ret
