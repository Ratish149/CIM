from django.db import models


class TrackType(models.TextChoices):
    MAKERSPACE = "Makerspace", "Makerspace (Room 1 · Schools & Teachers)"
    DESIGN_STUDIO = "Design Studio", "Design Studio (Room 2 · College Students)"
    GROWTH_ROOM = "Growth Room", "Growth Room (Room 3 · Business Owners)"


class RegistrationStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    CONTACTED = "Contacted", "Contacted"
    CONFIRMED = "Confirmed", "Confirmed"
    COMPLETED = "Completed", "Completed"
    CANCELLED = "Cancelled", "Cancelled"


class HeardAboutUs(models.TextChoices):
    AT_BIRAT_EXPO = "At Birat Expo", "At Birat Expo"
    CIM_WEBSITE = "CIM website", "CIM website"
    SOCIAL_MEDIA = "Facebook / social media", "Facebook / social media"
    SCHOOL_COLLEGE = "School / college", "School / college"
    FRIEND_COLLEAGUE = "Friend or colleague", "Friend or colleague"
    CIM_STAFF = "CIM member / staff", "CIM member / staff"
    NEWSPAPER_RADIO = "Newspaper / radio", "Newspaper / radio"
    OTHER = "Other", "Other"
