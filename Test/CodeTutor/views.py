import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
# Create your views here.


class TutorRegistrationForm(forms.ModelForm):

    # Stuff from AbstractUser
    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    mobile_number = forms.CharField(min_length=8, max_length=8)
    subjects_taught = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    tutor_qualification = forms.ModelChoiceField(queryset=Qualification.objects.all())
    hourly_rate = forms.IntegerField(min_value=0, max_value=1000)
    tutor_description = forms.CharField(widget=forms.Textarea(attrs={'rows':18, 'cols':36}))

    class Meta:
        model = Tutor  # Ensures Django knows which model this form is associated with
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'mobile_number',
            'subjects_taught',
            'tutor_qualification',
            'hourly_rate',
            'tutor_description'
        ]


class StudentRegistrationForm(forms.ModelForm):

    # Stuff from AbstractUser
    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    mobile_number = forms.CharField(min_length=8, max_length=8)
    location = forms.ChoiceField(choices=Student.location_choices)
    subjects_required = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = Student
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'mobile_number',
            'subjects_required'
        ]


def entry(request):
    if (request.method == 'GET' and not request.user.is_authenticated):
        return render(request, "CodeTutor/index.html", context={
            "tutor_registration_form": TutorRegistrationForm(),
            "student_registration_form": StudentRegistrationForm()
        })

    # IF somehow the tutor/student goes to the entry page when he is not supposed to, redirect him to the student list page
    # Not well coded sorry...
    elif (request.method == 'GET' and request.user.is_authenticated):
        if (Tutor.objects.filter(username=request.user.username)):
            return render(request, "CodeTutor/job_postings.html")
        else:
            # Yet to implement
            return logout_function(request)

    if (request.method == 'POST'):
        if ("student" in request.POST):
            student_registration_form = StudentRegistrationForm(request.POST)
            if (student_registration_form.is_valid()):
                return register_student(student_registration_form)
            else:
                return render(request, 'CodeTutor/index.html', {
                    "student_registration_form": student_registration_form
                })
        elif ("tutor" in request.POST):
            tutor_registration_form = TutorRegistrationForm(request.POST)
            if (tutor_registration_form.is_valid()):
                return register_tutor(tutor_registration_form)
            else:
                return render(request, 'CodeTutor/index.html', {
                    "tutor_registration_form": tutor_registration_form
                })
        elif ("login" in request.POST):
            return login_function(request)


def register_student(student_registration_form):
    new_student = Student.objects.create(
        username=student_registration_form.cleaned_data['username'],
        first_name=student_registration_form.cleaned_data['first_name'],
        last_name=student_registration_form.cleaned_data['last_name'],
        email=student_registration_form.cleaned_data['email'],
        mobile_number=student_registration_form.cleaned_data['mobile_number'],
        location=student_registration_form.cleaned_data['location'],
    )

    password = student_registration_form.cleaned_data['password']
    subjects_required = student_registration_form.cleaned_data['subjects_required']
    # Assign the many-to-many field after making the student object
    new_student.subjects_required.set(subjects_required)
    new_student.set_password(password)
    new_student.save()
    return HttpResponseRedirect(reverse("login_function"))


def register_tutor(tutor_registration_form):
    new_tutor = Tutor.objects.create(
        username=tutor_registration_form.cleaned_data['username'],
        first_name=tutor_registration_form.cleaned_data['first_name'],
        last_name=tutor_registration_form.cleaned_data['last_name'],
        email=tutor_registration_form.cleaned_data['email'],
        mobile_number=tutor_registration_form.cleaned_data['mobile_number'],
        tutor_qualification=tutor_registration_form.cleaned_data['tutor_qualification'],
        hourly_rate=tutor_registration_form.cleaned_data['hourly_rate'],
        tutor_description=tutor_registration_form.cleaned_data['tutor_description']
    )

    password = tutor_registration_form.cleaned_data['password']
    subjects_taught = tutor_registration_form.cleaned_data['subjects_taught']
    # Assign the many-to-many field after making the student object
    new_tutor.subjects_taught.set(subjects_taught)
    new_tutor.set_password(password)
    new_tutor.save()
    return HttpResponseRedirect(reverse("login_function"))


def login_function(request):
    if (request.method == "GET"):
        return render(request, 'CodeTutor/index.html')

    elif (request.method == "POST"):
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            # If the user with this username is a tutor, bring him to the student list view
            if (Tutor.objects.filter(username=username)):
                return HttpResponseRedirect(reverse("job_postings"))
            elif (Student.objects.filter(username=username)):
                return logout_function(request) # Should go student_main page but yet to implement

            # Otherwise, bring to tutor list view (tbc)
            return HttpResponseRedirect(reverse("tutor_main"))
        else:
            return render(request, "CodeTutor/index.html", {
                "message": "Invalid username and/or password."
            })


@login_required
def job_postings(request):
    if (request.method == "GET"):
        return render(request, "CodeTutor/job_postings.html")


@login_required
def load_student_profiles(request):
    if (request.method == "GET"):
        # Get start and end profiles
        start = int(request.GET.get('start') or 0)
        end = int(request.GET.get('end') or (start + 9))

        # Generate list of profiles
        data = []
        for i in range(start, end + 1):
            try:
                # Try to get 10 profiles at a time
                data.append(Student.objects.all()[i].serialize())
            except:
                # If not possible to get 10 profiles, break
                break
        print(data)
        # Artificially delay speed of response
        time.sleep(1)
        return JsonResponse(data, safe=False)


def logout_function(request):
    logout(request)
    return HttpResponseRedirect(reverse("entry"))

