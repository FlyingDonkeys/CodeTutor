from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
# Create your views here.


class TutorRegistrationForm(forms.ModelForm):
    mobile_number = forms.CharField(min_length=8, max_length=8)
    subjects_taught = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    tutor_qualification = forms.ModelChoiceField(queryset=Qualification.objects.all())
    hourly_rate = forms.IntegerField(min_value=0, max_value=1000)
    tutor_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Tutor  # Ensures Django knows which model this form is associated with
        fields = ['subjects_taught', 'tutor_qualification']


class StudentRegistrationForm(forms.ModelForm):
    mobile_number = forms.CharField(min_length=8, max_length=8)
    location = forms.ChoiceField(choices=Student.location_choices)
    subjects_required = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = Student
        fields = ['subjects_required']


def index(request):
    return render(request, "CodeTutor/layout.html")

def register(request):
    if (request.method == 'GET'):
        page_type = request.GET.get('type')
        # Check the value of the parameter and render different templates
        if page_type == 'tutor':
            return render(request, 'CodeTutor/registerTutor.html', context={
                "tutor_registration_form": TutorRegistrationForm()
            })
        elif page_type == 'student':
            return render(request, 'CodeTutor/registerStudent.html', context={
                "student_registration_form": StudentRegistrationForm()
            })


    else:
        print("balls")
