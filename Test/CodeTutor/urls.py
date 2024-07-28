from django.urls import path

from . import views

urlpatterns = [
    path("", views.entry, name="entry"),

    # Note that we need to connect with the server in order to login/logout
    path("login", views.login_function, name="login_function"),
    path("logout", views.logout_function, name="logout_function"),
    path("work_in_progress", views.work_in_progress, name="work_in_progress"),
    path("success/<str:user_type>", views.success, name="success"),
    path("create_profile", views.create_profile, name="create_profile"),

    # Loads the tutor page
    path("student_list", views.student_list, name="student_list"),
    # Loads the student page
    path("tutor_list", views.tutor_list, name="tutor_list"),
    path("data", views.data, name="data"),
    # Loads the page for Students to view their Tutors (for evaluation)
    path("my_tutors", views.my_tutors, name="my_tutors"),
    # Student profiles
    path("my_students", views.my_students, name="my_students"),
    # Loads the evaluation form for Students to evaluate a particular Tutor
    path("evaluate/<str:tutor_username>", views.evaluate, name="evaluate"),
    # API endpoint to retrieve student profiles dynamically on tutor main page
    path("load_student_profiles", views.load_student_profiles, name="load_student_profiles"),
    # API endpoint to retrieve tutor profiles dynamically on tutor main page
    path("load_tutor_profiles", views.load_tutor_profiles, name="load_tutor_profiles"),
    # API endpoint to retrieve list of subjects
    path("load_subjects", views.load_subjects, name="load_subjects"),
    # Path for tutor to apply to tutor a particular student
    path("apply/<str:student_username>", views.apply, name="apply"),
    # Path for student to apply to hire a particular tutor
    path("hire_tutor/<str:tutor_username>", views.hire_tutor, name="hire_tutor"),

    # Path for tutor to view the hiring requests he received from students
    path("received_hiring_requests", views.received_hiring_requests, name="received_hiring_requests"),
    # Path for student to view the tutor requests 
    path("received_tutor_requests", views.received_tutor_requests, name="received_tutor_requests"),
    # API endpoint to accept a hiring/application request
    path("accept/<str:type_of_application>/<int:application_id>", views.accept, name="accept"),
    # API endpoint to reject a hiring/application request
    path("reject/<str:type_of_application>/<int:application_id>", views.reject, name="reject"),

    #change the active state of students
    path("change_active_state",views.change_active_state, name="change_active_state"),

    #Product page for STRIPE
    path("product_page/<str:kwarg>/", views.product_page, name="product_page"),
    #Path to product page
    path("subscribe", views.subsribe, name="subscribe"),
    #redirect to successful after payment
    path("payment_successful", views.payment_successful, name="payment_successful"),
    #redirect to cancelled if payment is cancelled
    path("payment_cancelled", views.payment_cancelled, name="payment_cancelled"),
    #for STRIPEAPI to call do not modify
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    #API endpoint to retrive current user's profile information
    path('profile', views.profile,name = "profile"),
    path('load_user_profile', views.load_user_profile,name = "load_user_profile"),

    # Google login urls

]