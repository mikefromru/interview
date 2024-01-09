from django.db import models
from django.dispatch import receiver

def upload_path(instance, name):
    return f'images/{instance}/{name}'

class Subject(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_path)

    def __str__(self):
        return self.name

class Question(models.Model):

    name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    en_lang = models.CharField(max_length=500, blank=True, null=True)
    ru_lang = models.CharField(max_length=500, blank=True, null=True)
    en_answer = models.TextField(blank=True, null=True)
    ru_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.en_lang
