from django.db import models
import uuid 

class Person(models.Model):
    username = models.CharField(null= False, max_length=20, unique=True)
    password = models.CharField(null= False, max_length=20)
    code = models.CharField(null = False, max_length=10, default= uuid.uuid4().hex[:6].upper(), unique=True)
    class Meta:
        abstract = True

class Student(Person):
    
    class Meta:
        ordering = ['username']

class Tutor(Person):
    tutorScore = models.FloatField(null = False, default=10.00,unique=False)
