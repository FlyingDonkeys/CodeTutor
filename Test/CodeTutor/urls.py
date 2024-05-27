from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registerStudent", views.register, name="register"),
    path("registerTutor", views.register, name="register")
]