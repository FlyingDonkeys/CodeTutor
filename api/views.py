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
        data = request.data 

        username = data['username']
        location = data['location']
        password = data['password']
        subjects_arr = data.getlist('subjects_required')
        image = None
        if 'image' in data:
            image = data['image']

        queryset = Student.objects.filter(user_info__username=username)
        if queryset.exists():
            return Response({'Bad Request': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username, password=password)
            student = Student(user_info=user, location=location, image = image)
            student.save()
            subjects = Subject.objects.filter(subject_name__in=subjects_arr)
            for subject in subjects:
                student.subjects_required.add(subject)
            student.save()
            serialized_student = StudentSerializer(student)
            auth.login(request,user)
            request.session['code'] = student.code
            return Response(serialized_student.data, status=status.HTTP_201_CREATED)

class UpdateStudentView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    lookup_url_kwarg = 'code'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data 
        code = request.session.get('code','default_code')
        if code == 'default_code':
            print("code doesnt exist")
        
        username = data['username']
        location = data['location']
        password = data['password']
        subjects_arr = data.getlist('subjects_required')
        image = None
        if 'image' in data:
            image = data['image']

        queryset = Student.objects.filter(code=code)
        if not queryset.exists():
            return Response({'Bad Request': 'Username doesnt exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            student = queryset.first()
            user = student.user_info
            user.username = username
            if password:
                user.set_password(password)
            user.save()
            student.location = location
            student.save()
            temp = student.subjects_required.all()
            for t in temp:
                student.subjects_required.remove(t)
            subjects = Subject.objects.filter(subject_name__in=subjects_arr)
            for subject in subjects:
                student.subjects_required.add(subject)
            if image is not None:
                student.image = image
            student.save()
            serialized_student = StudentSerializer(student)
            auth.login(request,user)
            request.session['code'] = code
            return Response(serialized_student.data, status=status.HTTP_201_CREATED)

class GetStudentView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format = None):
        code = request.session.get('code','default_code')
        if code != 'default_code':
            student = Student.objects.filter(code = code)
            if len(student) > 0:
                data = StudentSerializer(student[0]).data
                request.session['code'] = code
                return Response(data,status = status.HTTP_200_OK)
            return Response({'Student Not Found':'Invalid Student Username'}, status = status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Username not found in request'}, status = status.HTTP_400_BAD_REQUEST)
    
class GetStudentViewUsername(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'username'

    def post(self, request, format = None):

        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            student = Student.objects.filter(user_info__username=username)
            if len(student) > 0:
                user = auth.authenticate(username=username, password=request.data['password'])
                if user is not None:
                    data = TutorSerializer(student.first()).data
                    auth.login(request, user)
                    request.session['code'] = student.first().code
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'Invalid Password': 'Wrong Password'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'Student Not Found':'Invalid Student Username'}, status = status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request':'Username not found in request'}, status = status.HTTP_400_BAD_REQUEST)


#TutorAPI

class TutorView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


class CreateTutorView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data
        
        username = data['username']
        password = data['password']
        subjects_arr = data.getlist('subjects_taught')
        image = None
        if 'image' in data:
            image = data['image']
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
            for subject in subjects_taught:
                tutor.subjects_taught.add(subject)
            tutor.save()
            serialized_tutor = TutorSerializer(tutor)
            auth.login(request,user)
            request.session['code'] = tutor.code
            return Response(serialized_tutor.data, status=status.HTTP_201_CREATED)


class UpdateTutorView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.IsAuthenticated, )
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        data = request.data  
        code = request.session.get('code','default_code')
        username = data['username']
        password = data['password']
        subjects_arr = data.getlist('subjects_taught')
        qual = data['tutor_qualification']
        hourly_rate = data['hourly_rate']
        tutor_description = data['tutor_description']
        image = None
        if 'image' in data:
            image = data['image']
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
            temp = tutor.subjects_taught.all()
            for t in temp:
                tutor.subjects_taught.remove(t)
            subjects_taught = Subject.objects.filter(subject_name__in=subjects_arr)
            for subject in subjects_taught:
                tutor.subjects_taught.add(subject)
            tutor.tutor_qualification = qual
            if image is not None:
                tutor.image = image
            tutor.save()
            serialized_tutor = TutorSerializer(tutor)
            auth.login(request,user)
            request.session['code'] = code
            return Response(serialized_tutor.data, status=status.HTTP_200_OK)


class GetTutorView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TutorSerializer
    lookup_url_kwarg = 'code'
    def get(self, request, format=None):

        #code = request.GET.get(self.lookup_url_kwarg)
        code = request.session.get('code','default_code')
        if code != 'default_code':
            tutor = Tutor.objects.filter(code=code)
            if tutor.exists():
                data = TutorSerializer(tutor[0]).data
                request.session['code'] = code
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
            tutor = Tutor.objects.filter(user_info__username=username)
            data = request.data
            if tutor.exists():
                user = auth.authenticate(username=username, password=data['password'])
                if user is not None:
                    data = TutorSerializer(tutor.first()).data
                    auth.login(request, user)
                    request.session['code'] = tutor.first().code
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
    permission_classes = (permissions.IsAuthenticated, )
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })