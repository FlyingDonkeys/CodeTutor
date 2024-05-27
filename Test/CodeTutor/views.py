from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
    return render(request, "CodeTutor/layout.html")

def register(request):
    return render(request, "CodeTutor/register.html")
