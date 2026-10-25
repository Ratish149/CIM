from accounts.models import CustomUser


def change_user_password_by_email(email: str, new_password: str) -> CustomUser:
    """
    Updates the password for a user identified by email.
    Raises CustomUser.DoesNotExist if the user is not found.
    """
    user = CustomUser.objects.filter(email__iexact=email.strip()).first()
    if not user:
        raise CustomUser.DoesNotExist(f"User with email '{email}' does not exist.")

    user.set_password(new_password)
    user.save(update_fields=["password"])
    return user
