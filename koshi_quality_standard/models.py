from django.db import models

# Create your models here.
class Requirement(models.Model):
    name = models.CharField(max_length=255,default="")

    def __str__(self):
        return self.name

class Question(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name="questions",null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    points = models.FloatField(null=True,blank=True,default=0)

    def __str__(self):
        return self.text

class Response(models.Model):
    name=models.CharField(max_length=255,default="")
    email=models.EmailField(null=True,blank=True)
    phone=models.CharField(max_length=255,null=True,blank=True)
    response_data=models.JSONField(null=True,blank=True)
    earned_points=models.FloatField(null=True,blank=True)
    category=models.CharField(max_length=255,null=True,blank=True)
    file_url=models.CharField(max_length=255,null=True,blank=True)
    percentage=models.FloatField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class ContactForm(models.Model):
    name=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=255)
    email=models.EmailField()
    subject=models.CharField(max_length=255)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

