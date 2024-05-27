from django.db import models
import uuid 

class Person(models.Model):
    def generate_code():
        while(True):
            code = uuid.uuid4().hex[:6].upper()
            print(Person.objects.filter(code=code))
            if(Person.objects.filter(code=code).count()==0):
                break
        print(code)
        return code
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
