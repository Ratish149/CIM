from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class InformationCategory(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class FAQ(BaseModel):
    category = models.ForeignKey(InformationCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

class Information(BaseModel):
    category = models.ForeignKey(InformationCategory, on_delete=models.CASCADE, related_name='information')
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Information"
        verbose_name_plural = "Information"

class ContentItem(BaseModel):
    CONTENT_TYPE = [
        ('Article', 'Article'),
        ('Video', 'Video'),
        ('Podcast', 'Podcast'),
        ('Infographic', 'Infographic'),
        ('Other', 'Other')
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    external_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE, default='Article')
    category = models.ForeignKey(InformationCategory, on_delete=models.CASCADE, related_name='content_items')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
