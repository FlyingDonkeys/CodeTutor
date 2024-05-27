from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Subject(models.Model):
    subject_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.subject_name}"


class Qualification(models.Model):
    type_of_qualification = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type_of_qualification}"


class CommonUser(AbstractUser):
    # Might need to handle for invalid phone numbers
    mobile_number = models.CharField(max_length=8)


class Student(CommonUser):
    # Minimum requirement without use of Google Maps
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
    location = models.CharField(choices=location_choices, max_length=64)
    subjects_required = models.ManyToManyField(Subject, related_name="students")

    class Meta:
        verbose_name = "Student"



class Tutor(CommonUser):
    subjects_taught = models.ManyToManyField(Subject, related_name="tutors")
    tutor_qualification = models.ForeignKey(Qualification, related_name='tutors', on_delete=models.CASCADE)
    hourly_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    # You could choose not to put a description ig
    tutor_description = models.TextField(blank=True)
    tutor_score = models.IntegerField(default=0)
    students_taught = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Tutor"
