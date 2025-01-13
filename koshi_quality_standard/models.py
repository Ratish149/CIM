from django.db import models

# Create your models here.
class Requirement(models.Model):
    name = models.CharField(max_length=255,default="")

    def __str__(self):
        return self.name

class Question(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name="questions",null=True,blank=True)
    text = models.CharField(null=True,blank=True,max_length=255)
    points = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.text


