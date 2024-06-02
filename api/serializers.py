from rest_framework import serializers
from .models import *
from django import forms

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id', 'subject_name']

##############PERSON SERIALIZERS###################
##USE PERSON DATA TO SEE IF USER IS STUDENT OR TUTOR#####
### IF TUTOR/STUDENT AND NEED MORE DATA SEND A SECOND REQUEST #####

##################STUDENT SERIALIZERS##############
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username','password','code','date_joined','subjects_required','isStudent','image')

class StudentRegistrationForm(forms.ModelForm):

    # Stuff from AbstractUser
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
    location = forms.ChoiceField(choices=Student.location_choices)
    subjects_required = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = Student
        fields = [
            'username',
            'password',
            'location',
            'subjects_required',
            'isStudent'
        ]
##################TUTOR SERIALIZERS##############
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('username','password','code','isStudent','date_joined','image')



