import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import serializers

from accounts.models import CustomUser, PasswordResetCode


def generate_numeric_code(length: int = 6) -> str:
    """Generates a cryptographically secure numeric verification code."""
    return "".join(secrets.choice("0123456789") for _ in range(length))


def create_and_send_password_reset_code(email: str) -> PasswordResetCode:
    """
    Creates a new 6-digit password reset verification code for the user
    and sends it via email using the password_reset_code.html template.
    Invalidates previously active codes.
    """
    user = CustomUser.objects.filter(email__iexact=email.strip()).first()
    if not user:
        raise serializers.ValidationError({
            "email": "User with this email does not exist."
        })

    # Invalidate previous unused codes for this user
    PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)

    code = generate_numeric_code(6)
    expires_at = timezone.now() + timedelta(minutes=15)

    reset_code = PasswordResetCode.objects.create(
        user=user,
        code=code,
        expires_at=expires_at,
    )

    # Render template for email
    subject = "Password Reset Verification Code - CIM"
    context = {
        "user_name": user.first_name or user.username,
        "email": user.email,
        "code": code,
        "valid_minutes": 15,
    }
    html_message = render_to_string(
        "accounts/emails/password_reset_code.html", context
    )
    plain_message = (
        f"Namaste {user.first_name or user.username},\n\n"
        f"You requested to reset the password for your CIM account ({user.email}).\n\n"
        f"Your verification code is: {code}\n\n"
        f"This code will expire in 15 minutes.\n"
        f"If you did not request a password reset, please ignore this email.\n\n"
        f"Best regards,\nThe CIM Team"
    )

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", None
    )

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as exc:
        raise serializers.ValidationError(
            f"Failed to send verification email. Error: {str(exc)}"
        )

    return reset_code


def resend_password_reset_code(email: str) -> PasswordResetCode:
    """
    Resends a new password reset verification code to the user's email,
    invalidating any previously generated codes.
    """
    return create_and_send_password_reset_code(email)


def verify_password_reset_code(email: str, code: str) -> PasswordResetCode:
    """
    Validates that a verification code exists, is unused, and has not expired.
    """
    user = CustomUser.objects.filter(email__iexact=email.strip()).first()
    if not user:
        raise serializers.ValidationError({
            "email": "User with this email does not exist."
        })

    reset_record = (
        PasswordResetCode.objects.filter(
            user=user,
            code=code.strip(),
            is_used=False,
        )
        .order_by("-created_at")
        .first()
    )

    if not reset_record:
        raise serializers.ValidationError({
            "code": "Invalid verification code or code has already been used."
        })

    if timezone.now() > reset_record.expires_at:
        raise serializers.ValidationError({
            "code": "Verification code has expired. Please request a new one."
        })

    return reset_record


def reset_password_with_code(email: str, code: str, new_password: str) -> CustomUser:
    """
    Validates verification code and updates the user's password.
    Marks the code as used.
    """
    reset_record = verify_password_reset_code(email=email, code=code)
    user = reset_record.user

    user.set_password(new_password)
    user.save(update_fields=["password"])

    reset_record.is_used = True
    reset_record.save(update_fields=["is_used"])

    return user
