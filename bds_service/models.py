from django.db import models

# Create your models here.
class BDSCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
class Tags(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BDSService(models.Model):
    FINANCE_CHOICES = [
        ('Meet your VCs', 'Meet your VCs'),
        ('Meet your Banks', 'Meet your Banks'),
    ]
    Company_name = models.CharField(max_length=255)
    finance_services=models.CharField(max_length=255, choices=FINANCE_CHOICES,null=True,blank=True)
    service=models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(BDSCategory, on_delete=models.SET_NULL, null=True)
    address=models.CharField(max_length=255)
    tags=models.ManyToManyField(Tags)
    logo = models.FileField(upload_to='bds_service_logos/', blank=True, null=True)

    def __str__(self):
        return f'{self.Company_name} - {self.service}'