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
        
class Session(models.Model):
    title=models.CharField(max_length=200)
    questions=models.ManyToManyField(Question,blank=True)
    is_acepting_questions=models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def can_add_question(self):
        return self.is_acepting_questions  # Check if questions can be added
   
class RunningSession(models.Model):
    session=models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Running Session"
        verbose_name_plural = "Running Sessions"

    def save(self, *args, **kwargs):
        if not self.pk and RunningSession.objects.exists():
            raise ValueError("There can be only one RunningSession instance.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.session.title

class Voting(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " voted on " + self.question.name
