from django.db import models
from accounts.models import CustomUser

class Tag(models.Model):
    name=models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    thumbnail = models.FileField(upload_to='event_thumbnails/', null=True, blank=True)
    location = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='events', blank=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Attendee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Sponsor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sponsors')
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='sponsor_logos/', null=True, blank=True)
    website = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class AgendaItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='agenda_items')
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True,null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    speaker = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return f"{self.time} - {self.title} ({self.event.title})"