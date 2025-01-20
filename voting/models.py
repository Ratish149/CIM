from django.db import models

# Create your models here.
class Question(models.Model):
    name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15)
    question_text=models.TextField()
    vote_count=models.IntegerField(default=0,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " asked " + self.question_text

class Voting(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " voted on " + self.question.name
