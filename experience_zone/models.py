from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from wish_and_offers.models import HSCode, SubCategory


class ExperienceZoneBooking(models.Model):
    title = models.CharField(max_length=200, default="")
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, null=True, blank=True)
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="experience_zone_subcategories",
        blank=True,
        null=True,
    )
    preferred_month = models.DateField(
        help_text="First day of the month for which booking is requested"
    )
    description = models.TextField(
        help_text="Details about products, innovations, or skills to be displayed"
    )
    product = models.ForeignKey(
        HSCode,
        on_delete=models.CASCADE,
        related_name="experience_zone_hscode",
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=10,
        choices=[("Product", "Product"), ("Service", "Service")],
        default="Product",
    )

    status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Experience Zone Booking")
        verbose_name_plural = _("Experience Zone Bookings")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.company_name} - {self.preferred_month.strftime('%B %Y')}"
