from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/<str:user_type>", views.register, name="register"),
    path("login", views.login_function, name="login_function"),
    path("logout", views.logout_function, name="logout_function")
]