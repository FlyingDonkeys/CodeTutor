from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid 
import datetime
from django.utils import timezone

class Subject(models.Model):

    SUBJECT_CHOICES = [
        ('H2_MATHEMATICS', 'H2 Mathematics'),
        ('H2_PHYSICS', 'H2 Physics'),
        ('H2_CHEMISTRY', 'H2 Chemistry'),
        ('H2_ECONOMICS', 'H2 Economics'),
    ]

    subject_name = models.CharField(
    max_length=64,
    choices=SUBJECT_CHOICES,
    unique=True
    )

    def __str__(self):
        return f"{self.subject_name}"


class Qualification(models.Model):
    type_of_qualification = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type_of_qualification}"

class Person(models.Model):

    def generate_code():

        while(True):

            code = uuid.uuid4().hex[:6].upper()

            print(Person.objects.filter(code=code))

            if(Person.objects.filter(code=code).count()==0):

                break

        print(code)

        return code
    
    image = models.ImageField(upload_to='./uploads/images', null=True, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    password = models.CharField(null= False, max_length=20)

    code = models.CharField(null = False, max_length=10, default= uuid.uuid4().hex[:6].upper(), unique=True)

    
    
    class Meta:
        abstract = True

class Student(Person):
    location_choices = {
        "N": "North",
        "NE": "North East",
        "E": "East",
        "SE": "South East",
        "S": "South",
        "SW": "South West",
        "W": "West",
        "NW": "North West",
        "C": "Central"
    }
    isStudent = models.BooleanField(default=True)
    username = models.CharField(null= False, max_length=20, unique=True)
    location = models.CharField(default='N', choices=location_choices, max_length=64)
    subjects_required = models.ManyToManyField(Subject, related_name="students")
    class Meta:
        ordering = ['username']


class Tutor(Person):
    username = models.CharField(null= False, max_length=20, unique=True)
    isStudent = models.BooleanField(default=False)
    subjects_taught = models.ManyToManyField(Subject, related_name="tutors")
    tutor_qualification = models.CharField(default="", unique=False, max_length=100)
    hourly_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        default= 0
    )
    # You could choose not to put a description iggg
    tutor_description = models.TextField(blank=True)
    tutor_score = models.IntegerField(default=0)
    students_taught = models.IntegerField(default=0)
    class Meta:
        ordering = ['username']
  
