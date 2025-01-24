from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.name
    
class Newsletter(models.Model):
    email = models.EmailField()
    subscribed=models.BooleanField(default=True)

    def __str__(self):
        return self.email

