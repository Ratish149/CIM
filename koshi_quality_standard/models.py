from django.db import models

# Create your models here.
class Question(models.Model):
    CATEGORY=[
        ('OFI','Opportunity For Improvement'),
        ('O','Observation'),
        ('M','Major'),
        ('C','Critical')
    ]
    question_text = models.CharField(max_length=200)
    category=models.CharField(max_length=50, choices=CATEGORY)

    def __str__(self):
        return self.question_text

class Document(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    document_name=models.CharField(max_length=200)
    points=models.FloatField()

    def __str__(self):
        return f'{self.question.question_text} - {self.document_name} - {self.points}'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    document=models.ForeignKey(Document, on_delete=models.CASCADE)
    submission=models.ForeignKey('SavedAnswer', on_delete=models.CASCADE, null=True, blank=True)
    is_true=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.document} - {self.is_true}'
    
class SavedAnswer(models.Model):
    total_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Saved Answer {self.id} - Score: {self.total_score}'


