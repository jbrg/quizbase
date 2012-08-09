from django.db import models

# Create your models here.

class Collection(models.Model):
    name = models.CharField(max_length=255)
    #author = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Card(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    collection = models.ForeignKey(Collection)
    def __unicode__(self):
        return self.name
