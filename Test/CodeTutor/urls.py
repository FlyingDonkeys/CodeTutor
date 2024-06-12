from django.urls import path

from . import views

urlpatterns = [
    path("", views.entry, name="entry"),

    # Note that we need to connect with the server in order to login/logout
    path("login", views.login_function, name="login_function"),
    path("logout", views.logout_function, name="logout_function"),
    path("work_in_progress", views.work_in_progress, name="work_in_progress"),
    path("success", views.success, name="success"),

    # Loads the tutor page
    path("job_postings", views.job_postings, name="job_postings"),
    # API endpoint to retrieve student profiles dynamically on tutor main page
    path("load_student_profiles", views.load_student_profiles, name="load_student_profiles"),
    # Path for tutor to apply to tutor a particular student
    path("apply/<str:student_username>", views.apply, name="apply")
]