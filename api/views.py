from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from .models import Student,Tutor
from .serializers import StudentSerializer,TutorSerializer, CreateStudentSerializer, CreateTutorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
#StudentAPI 
class StudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CreateStudentView(APIView):
    serializer_class = CreateStudentSerializer
    def post(self, request, format = None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data = request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            queryset = Student.objects.filter(username = username)
            if queryset.exists():
                student = queryset[0]
                return Response(StudentSerializer(student).data, status = status.HTTP_400_BAD_REQUEST)
            else:
                student = Student(username = username, password = password)
                student.save()
                return Response(StudentSerializer(student).data, status = status.HTTP_201_CREATED)
        return Response({'Bad Request':'Invalid data...'}, status = status.HTTP_400_BAD_REQUEST)

#TutorAPI
class TutorView(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer