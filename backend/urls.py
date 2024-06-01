
from django.urls import path
from .views import StudentView,TutorView,CreateStudentView, GetStudentView, SubjectList, GetStudentViewUsername, UpdateStudentView, UpdateTutorView, CreateTutorView, GetTutorViewUsername, GetTutorView
urlpatterns = [
    path('student', StudentView.as_view()),
    path('tutor', TutorView.as_view()),
    path('subjects', SubjectList.as_view(), name='subjects_list'),

    path('get-student',GetStudentView.as_view()),
    path('get-student-username',GetStudentViewUsername.as_view()),
    path('create-student', CreateStudentView.as_view()),
    path('update-student',UpdateStudentView.as_view()),

    path('get-tutor',GetTutorView.as_view()),
    path('get-tutor-username',GetTutorViewUsername.as_view()),
    path('create-tutor', CreateTutorView.as_view()),
    path('update-tutor',UpdateTutorView.as_view())
]
