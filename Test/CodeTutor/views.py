import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
from django.contrib import messages
# Create your views here.


class TutorRegistrationForm(forms.ModelForm):

    # Stuff from AbstractUser
    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    mobile_number = forms.CharField(min_length=8, max_length=8)
    profile_picture = forms.ImageField(required=False)

    subjects_taught = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    tutor_qualification = forms.ModelChoiceField(queryset=Qualification.objects.all())
    hourly_rate = forms.IntegerField(min_value=0, max_value=1000)
    tutor_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':18, 'cols':36}))

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
            'tutor_description',
            'profile_picture'
        ]


class StudentRegistrationForm(forms.ModelForm):

    # Stuff from AbstractUser
    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    mobile_number = forms.CharField(min_length=8, max_length=8)
    profile_picture = forms.ImageField(required=False)

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
            'subjects_required',
            'profile_picture'
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
            return render(request, "CodeTutor/work_in_progress.html")

    if (request.method == 'POST'):
        if ("student" in request.POST):
            student_registration_form = StudentRegistrationForm(request.POST, request.FILES)
            if (student_registration_form.is_valid()):
                return register_student(request, student_registration_form)
            else:
                return render(request, 'CodeTutor/index.html', {
                    "student_registration_form": student_registration_form,
                    "tutor_registration_form": TutorRegistrationForm,
                    "student_error": True,
                    "tutor_error": False
                })
        elif ("tutor" in request.POST):
            tutor_registration_form = TutorRegistrationForm(request.POST, request.FILES)
            if (tutor_registration_form.is_valid()):
                return register_tutor(request, tutor_registration_form)
            else:
                return render(request, 'CodeTutor/index.html', {
                    "tutor_registration_form": tutor_registration_form,
                    "student_registration_form": StudentRegistrationForm,
                    "tutor_error": True,
                    "student_error": False
                })
        elif ("login" in request.POST):
            return login_function(request)


def register_student(request, student_registration_form):
    new_student = Student.objects.create(
        username=student_registration_form.cleaned_data['username'],
        first_name=student_registration_form.cleaned_data['first_name'],
        last_name=student_registration_form.cleaned_data['last_name'],
        email=student_registration_form.cleaned_data['email'],
        mobile_number=student_registration_form.cleaned_data['mobile_number'],
        location=student_registration_form.cleaned_data['location'],
        profile_picture=student_registration_form.cleaned_data['profile_picture']
    )

    password = student_registration_form.cleaned_data['password']
    subjects_required = student_registration_form.cleaned_data['subjects_required']
    # Assign the many-to-many field after making the student object
    new_student.subjects_required.set(subjects_required)
    new_student.set_password(password)
    new_student.save()

    return HttpResponseRedirect(reverse("login_function"))


def register_tutor(request, tutor_registration_form):
    new_tutor = Tutor.objects.create(
        username=tutor_registration_form.cleaned_data['username'],
        first_name=tutor_registration_form.cleaned_data['first_name'],
        last_name=tutor_registration_form.cleaned_data['last_name'],
        email=tutor_registration_form.cleaned_data['email'],
        mobile_number=tutor_registration_form.cleaned_data['mobile_number'],
        tutor_qualification=tutor_registration_form.cleaned_data['tutor_qualification'],
        hourly_rate=tutor_registration_form.cleaned_data['hourly_rate'],
        tutor_description=tutor_registration_form.cleaned_data['tutor_description'],
        profile_picture=tutor_registration_form.cleaned_data['profile_picture']
    )

    password = tutor_registration_form.cleaned_data['password']
    subjects_taught = tutor_registration_form.cleaned_data['subjects_taught']
    # Assign the many-to-many field after making the student object
    new_tutor.subjects_taught.set(subjects_taught)
    new_tutor.set_password(password)
    new_tutor.save()

    # Use Django messages framework to pass context to the html
    messages.success(request, "You have successfully registered your tutor profile. Please proceed to login.")

    return HttpResponseRedirect(reverse("success"))


def login_function(request):
    if (request.method == "GET"):
        return render(request, 'CodeTutor/index.html', context={
            "tutor_registration_form": TutorRegistrationForm,
            "student_registration_form": StudentRegistrationForm
        })

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
                # Should go student_main page but yet to implement
                return HttpResponseRedirect(reverse("work_in_progress"))

            # Otherwise, bring to tutor list view (tbc)
            return HttpResponseRedirect(reverse("work_in_progress"))
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
        # Artificially delay speed of response
        time.sleep(1)
        return JsonResponse(data, safe=False)


def load_subjects(request):
    if (request.method == "GET"):
        subjects = []
        for subject in Subject.objects.all():
            subjects.append(subject.serialize())
        return JsonResponse(subjects, safe=False)
    else:
        return None
        # Throw an error, but I have no time to complete this yet


@login_required()
def apply(request, student_username):
    if (request.method == "GET"):
        return render(request, 'CodeTutor/apply.html', context=
            {'student': Student.objects.get(username=student_username)}
        )
    # After receiving the form. we have to send the tutor's application to the student
    # I guess it is timely to include a new model to meet this requirement
    # Each Student may be related to several Applications
    elif (request.method == "POST"):

        # Extract information from the application form
        information = request.POST
        selected_subject = information.get('selected_subject')
        tutor_description = information.get('tutor_description')
        tutor_rates = information.get('tutor_rates')

        # Create new Application object
        application = Application(subject=Subject.objects.get(subject_name=selected_subject),
                                  application_description=tutor_description,
                                  tutor_rates=tutor_rates,
                                  tutor=Tutor.objects.get(username=request.user.username),
                                  student=Student.objects.get(username=student_username)
                                  )
        application.save()

        messages.success(request, "Your application has been received successfully.")
        return HttpResponseRedirect(reverse('success'))


@login_required()
def logout_function(request):
    logout(request)
    return HttpResponseRedirect(reverse("entry"))


def work_in_progress(request):
    return render(request, 'CodeTutor/work_in_progress.html')


@login_required
def success(request):
    return render(request, 'CodeTutor/success.html')


