from django.urls import path

from . import views

urlpatterns = [
    path("", views.entry, name="entry"),

    # Note that we need to connect with the server in order to login/logout
    path("login", views.login_function, name="login_function"),
    path("logout", views.logout_function, name="logout_function"),
    path("tutor_main", views.tutor_main, name="tutor_main")
]