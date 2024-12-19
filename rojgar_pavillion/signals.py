from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Registration

@receiver(post_save, sender=Registration)
def send_registration_email(sender, instance, created, **kwargs):
    """
    Send confirmation email when a new registration is created
    """
    if created and instance.status == 'CONFIRMED':
        instance.send_confirmation_email() 