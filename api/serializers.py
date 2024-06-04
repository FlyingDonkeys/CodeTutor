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
    username = serializers.StringRelatedField(source='user_info.username')
    password = serializers.StringRelatedField(source='user_info.password')
    subjects_required = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = Student
        fields = ('username','password','code','date_joined','subjects_required','isStudent','image')

##################TUTOR SERIALIZERS##############
class TutorSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user_info.username')
    password = serializers.StringRelatedField(source='user_info.password')
    subjects_taught = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = Tutor
        fields = ('username','password','code','isStudent','date_joined','image','subjects_taught','tutor_description')



