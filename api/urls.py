
from django.urls import path
from .views import StudentView,TutorView,CreateStudentView
urlpatterns = [
    path('student', StudentView.as_view()),
    path('create-student', CreateStudentView.as_view()),
    path('tutor', TutorView.as_view())
]
