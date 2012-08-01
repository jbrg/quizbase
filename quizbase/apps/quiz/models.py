from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=255)
    #details = models.CharField(max_length=1024)
    def __unicode__(self):
        return self.question
    

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice = models.CharField(max_length=255)
    def __unicode__(self):
        return self.choice

class CorrectAnswer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Choice)
