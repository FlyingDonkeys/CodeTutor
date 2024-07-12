from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import serializers

# Create your models here.


class Subject(models.Model):
    subject_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.subject_name}"

    def serialize(self):
        return {
            "subject_name": self.subject_name
        }


class Qualification(models.Model):
    type_of_qualification = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type_of_qualification}"


class CommonUser(AbstractUser):
    # Might need to handle for invalid phone numbers
    mobile_number = models.CharField(max_length=8)
    # Each user to have a profile picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


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
    postal_code = models.IntegerField(default= 738090, validators=[
            MaxValueValidator(999999),
            MinValueValidator(100000)
        ])
    subjects_required = models.ManyToManyField(Subject, related_name="students")
    # Student will have a rate that they are willing to pay as well
    offered_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
        default=0
    )
    is_finding_tutor = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Student"

    def serialize(self):
        # Note that ImageFields cannot be serialised, so we pass the url to the Javascript to be converted to image there
        profile_picture_url = self.profile_picture.url if self.profile_picture else None
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_joined": self.date_joined,
            "location": self.location,
            "subjects_required": [subject.subject_name for subject in self.subjects_required.all()],
            "offered_rate": self.offered_rate,
            "is_finding_tutor": self.is_finding_tutor,
            "profile_picture_url": profile_picture_url,
            "postal_code":self.postal_code

        }


class Tutor(CommonUser):
    subjects_taught = models.ManyToManyField(Subject, related_name="tutors")
    tutor_qualification = models.ForeignKey(Qualification, related_name='tutors', on_delete=models.CASCADE)
    hourly_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
    )
    # You could choose not to put a description ig
    tutor_description = models.TextField(blank=True)
    tutor_score = models.DecimalField(max_digits=4, decimal_places=2, default=10.00)
    students_taught = models.IntegerField(default=0)

    # A tutor can have many students, just like how a student can have many tutors
    students = models.ManyToManyField(Student, related_name="tutors")

    # A tutor can also receive evaluations from many students (like how a student can evaluate many tutors)
    evaluators = models.ManyToManyField(Student, related_name="evaluated_tutors")

    class Meta:
        verbose_name = "Tutor"

    def serialize(self):
        # Note that ImageFields cannot be serialised, so we pass the url to the Javascript to be converted to image there
        profile_picture_url = self.profile_picture.url if self.profile_picture else None
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_joined": self.date_joined,
            "subjects_taught": [subject.subject_name for subject in self.subjects_taught.all()],
            "hourly_rate": self.hourly_rate,
            "profile_picture_url": profile_picture_url,
            "tutor_description": self.tutor_description,
            "tutor_score": self.tutor_score,
            "students_taught": self.students_taught,
            "students": [student.username for student in self.students.all()]
        }


# Django model to represent an Application by a Tutor to teach a Student
class Application(models.Model):
    # Stuff in application form
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    application_description = models.TextField(blank=True)
    tutor_rates = models.IntegerField(default=0)

    # Other stuff
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="sent_applications") # Tutor is related to his applications
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="received_applications") # Student related to received ones
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tutor.username} applied for {self.subject.subject_name} with {self.student.username}"


# Django model to represent a HiringApplication by a Student to hire a Tutor
class HiringApplication(models.Model):
    # Stuff collected in application form
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    offered_rates = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000)])

    # Other stuff to identify Student who wants to hire, and target Tutor
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="received_applications") # Tutor is related to his received applications
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sent_applications") # Student related to sent hiring ones
    application_date = models.DateTimeField(auto_now_add=True)


#Payment recording 
class UserPayment(models.Model):
    app_user = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

