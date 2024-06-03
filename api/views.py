from django.shortcuts import render
from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import permissions


class SubjectList(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        
        print(serializer.data)
        return Response(serializer.data)


# Create your views here.

#StudentAPI 
class StudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



class CreateStudentView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data  # Use request.data for POST data in DRF

        username = data['username']
        location = data['location']
        password = data['password']
        subjects_arr = data['subjects_required']
        image = data['image']

        queryset = Student.objects.filter(user_info__username=username)
        if queryset.exists():
            return Response({'Bad Request': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create and save the student instance first
            user = User.objects.create_user(username=username, password=password)
            student = Student(user_info=user, location=location, image = image)
            student.save()
            
            # Map subjects_arr to Subject instances and set the many-to-many relationship
            subjects_required = Subject.objects.filter(subject_name__in=subjects_arr)
            student.subjects_required.set(subjects_required)
            
            student.save()
            # Use the serializer to convert the student instance into JSON-friendly format
            serialized_student = StudentSerializer(student)
            auth.authenticate(username=username, password=password)
            return Response(serialized_student.data, status=status.HTTP_201_CREATED)

class UpdateStudentView(APIView):
    #permission_classes = [IsAuthenticated]
    #permission_classes = (permissions.IsAuthenticated, )
    
    lookup_url_kwarg = 'code'
    print("at Update")
    def post(self, request, format=None):
        print(request.user.is_authenticated)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data  # Use request.data for POST data in DRF
        print("test")
        code = request.GET.get(self.lookup_url_kwarg)
        username = data['username']
        location = data['location']
        password = data['password']
        subjects_arr = data['subjects_required']
        image = data['image']

        queryset = Student.objects.filter(code=code)
        if not queryset.exists():
            return Response({'Bad Request': 'Username doesnt exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            student = queryset.first()
            # Create and save the student instance first
            user = student.user_info
            user.username = username
            if password:
                user.set_password(password)
            user.save()

            student.location = location
            #student = Student(username=username, password=password, location=location)
            student.save()
            
            # Map subjects_arr to Subject instances and set the many-to-many relationship
            subjects_required = Subject.objects.filter(subject_name__in=subjects_arr)
            student.subjects_required.set(subjects_required)
            student.image = image
            
            student.save()
            # Use the serializer to convert the student instance into JSON-friendly format
            serialized_student = StudentSerializer(student)
            
            return Response(serialized_student.data, status=status.HTTP_201_CREATED)

class GetStudentView(APIView):
    #permission_classes = (permissions.IsAuthenticated, )
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format = None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            student = Student.objects.filter(code = code)
            if len(student) > 0:
                data = StudentSerializer(student[0]).data
                return Response(data,status = status.HTTP_200_OK)
            return Response({'Student Not Found':'Invalid Student Username'}, status = status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Username not found in request'}, status = status.HTTP_400_BAD_REQUEST)
    
class GetStudentViewUsername(APIView):
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'username'

    def post(self, request, format = None):
        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            student = Student.objects.filter(user_info__username=username)
            print(student)
            print(request.data['password'])
            if len(student) > 0:
                user = auth.authenticate(username=username, password=request.data['password'])
                print(user)
                if user is not None:
                    data = TutorSerializer(student.first()).data
                    auth.login(request, user)
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'Invalid Password': 'Wrong Password'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'Student Not Found':'Invalid Student Username'}, status = status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Username not found in request'}, status = status.HTTP_400_BAD_REQUEST)


#TutorAPI

class TutorView(generics.ListAPIView):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


class CreateTutorView(APIView):
    
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data
        
        username = data['username']
        password = data['password']
        subjects_arr = data['subjects_taught']
        image = data['image']
        print(image)
        qual = data['tutor_qualification']
  
        hourly_rate = data['hourly_rate']
        tutor_description = data['tutor_description']

        queryset = Tutor.objects.filter(user_info__username=username)
        if queryset.exists():
            return Response({'Bad Request': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username, password=password)
            tutor = Tutor(user_info = user, hourly_rate=hourly_rate, tutor_description=tutor_description,image=image, tutor_qualification =qual)
            tutor.save()
            
            subjects_taught = Subject.objects.filter(subject_name__in=subjects_arr)
            tutor.subjects_taught.set(subjects_taught)
            tutor.save()
            serialized_tutor = TutorSerializer(tutor)
            auth.authenticate(username=username, password=password)
            return Response(serialized_tutor.data, status=status.HTTP_201_CREATED)


class UpdateTutorView(APIView):
    #permission_classes = [IsAuthenticated]
    #permission_classes = (permissions.IsAuthenticated, )
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data
        code = request.GET.get(self.lookup_url_kwarg)
        username = data['username']
        password = data['password']
        subjects_arr = data['subjects_taught']
        qual = data['tutor_qualification']
        hourly_rate = data['hourly_rate']
        tutor_description = data['tutor_description']
        image = data['image']
        print(image)

        queryset = Tutor.objects.filter(code=code)
        if not queryset.exists():
            return Response({'Bad Request': 'Username does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            tutor = queryset.first()
            user = tutor.user_info
            user.username = username
            if password:
                user.set_password(password)
            user.save()
            tutor.hourly_rate = hourly_rate
            tutor.tutor_description = tutor_description
            tutor.save()
            
            subjects_taught = Subject.objects.filter(subject_name__in=subjects_arr)
            tutor.subjects_taught.set(subjects_taught)
            tutor.tutor_qualification = qual
            tutor.image = image
            tutor.save()

            serialized_tutor = TutorSerializer(tutor)
            return Response(serialized_tutor.data, status=status.HTTP_200_OK)


class GetTutorView(APIView):
    #permission_classes = [IsAuthenticated]
    #permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TutorSerializer
    lookup_url_kwarg = 'code'
    print("hello")
    def get(self, request, format=None):
        print("halo")
        code = request.GET.get(self.lookup_url_kwarg)
        if code is not None:
            print(code)
            tutor = Tutor.objects.filter(code=code)
            print(tutor)
            if tutor.exists():
                print(tutor[0])
                data = TutorSerializer(tutor[0]).data
                print(data)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Tutor Not Found': 'Invalid Tutor Code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code not found in request'}, status=status.HTTP_400_BAD_REQUEST)
    


class GetTutorViewUsername(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = TutorSerializer
    lookup_url_kwarg = 'username'

    def post(self, request, format=None):
        username = request.GET.get(self.lookup_url_kwarg)
        if username is not None:
            tutor = Tutor.objects.filter(user__username=username)
            data = request.data
            if tutor.exists():
                user = auth.authenticate(username=username, password=data['password'])
                if user is not None:
                    data = TutorSerializer(tutor.first()).data
                    auth.login(request, user)
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'Invalid Password': 'Wrong Password'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'Tutor Not Found': 'Invalid Tutor Username'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Username not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Loggout Out' })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })
        
#Crsf cookie 

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })
    
#Delete account
@csrf_exempt
class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })