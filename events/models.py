from django.db import models
from django.utils.text import slugify

from accounts.models import CustomUser


class SlugMixin:
    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        model = self.__class__
        while model.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(SlugMixin, models.Model):
    STATUS = (
        ("Published", "Published"),
        ("Draft", "Draft"),
        ("Cancelled", "Cancelled"),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    thumbnail = models.FileField(upload_to="event_thumbnails/", null=True, blank=True)
    location = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name="events", blank=True)
    organizer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="organized_events",
        null=True,
        blank=True,
    )
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Draft")
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Attendee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendees")
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Sponsor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sponsors")
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to="sponsor_logos/", null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"


class AgendaItem(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="agenda_items"
    )
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    speaker = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return f"{self.time} - {self.title} ({self.event.title})"
