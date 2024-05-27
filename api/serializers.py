from rest_framework import serializers
from .models import Student, Tutor

##################STUDENT SERIALIZERS##############
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username','password','code')

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username','password')
##################TUTOR SERIALIZERS##############
class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('username','password','code')

class CreateTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('username','password')

