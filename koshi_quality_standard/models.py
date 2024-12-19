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
        return f'{self.document_name} - {self.points}'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    document=models.ForeignKey(Document, on_delete=models.CASCADE)
    is_true=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.document} - {self.is_true}'
    