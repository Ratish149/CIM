from django.db import models

# Create your models here.
class BusinessCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class BusinessInformation(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(BusinessCategory, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name