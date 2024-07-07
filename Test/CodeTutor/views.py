import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import NumberInput, TextInput
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import *
from django import forms
from django.contrib import messages
from django.conf import settings
import stripe
import time


@login_required
def profile(request):
    return render(request, "CodeTutor/profile.html")


@login_required
def load_user_profile(request):
    if request.method == "GET":
        is_student = False
        user = None
        query_set = Student.objects.all().filter(username=request.user.username)
        if query_set.exists():
            is_student = True
            user = query_set.first()
            print(f"currently searching student db {query_set}")
            context = {
                'google_api_key': settings.GOOGLE_API_KEY,
                'is_student': is_student,
                'user': {
                    'username': user.username,
                    'id': user.id,
                    'location': user.location,
                    'postal_code': user.postal_code,
                    'profile_picture_url': user.profile_picture.url
                }
            }
            return JsonResponse(context, safe=False)
        else:
            query_set = Tutor.objects.all().filter(username=request.user.username)
            user = query_set[0]
            print(f"currently searching tutor db {user}")

        context = {
            'google_api_key': settings.GOOGLE_API_KEY,
            'is_student': is_student,
            'user': {
                'username': user.username,
                'id': user.id,
                'description': user.tutor_description,
                'profile_picture_url': user.profile_picture.url
            }
        }
        return JsonResponse(context, safe=False)


# STRIPE API
@login_required(login_url='login')
def product_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.PRODUCT_PRICE,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return render(request, 'CodeTutor/product_page.html')


# Goes here if successful,works only with real web address
## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    user_payment = UserPayment.objects.get(app_user=user_id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    return render(request, 'CodeTutor/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, 'CodeTutor/payment_cancelled.html')


# This is to be called by stripeAPI do not try to access the url
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
        user_payment.payment_bool = True
        user_payment.save()
    return HttpResponse(status=200)


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
    tutor_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 18, 'cols': 36}))

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
    postal_code = forms.IntegerField(required=True)
    subjects_required = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())
    offered_rate = forms.IntegerField(min_value=0, max_value=1000)

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
            'profile_picture',
            'postal_code',
            'offered_rate'
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
            return render(request, "CodeTutor/student_list.html")
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
        profile_picture=student_registration_form.cleaned_data['profile_picture'],
        offered_rate = student_registration_form.cleaned_data['offered_rate']
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

    return HttpResponseRedirect(reverse("login_function"))


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
                return HttpResponseRedirect(reverse("student_list"))
            elif (Student.objects.filter(username=username)):
                # Should go student_main page but yet to implement
                return HttpResponseRedirect(reverse("tutor_list"))

            # Otherwise, the user is an admin, but we dont care abt this
            return HttpResponseRedirect(reverse("work_in_progress"))
        else:
            return render(request, "CodeTutor/index.html", {
                "message": "Invalid username and/or password."
            })


# Note that only tutors should be able to view this page
@login_required
def student_list(request):
    if (request.method == "GET"):
        tutor = Tutor.objects.get(username=request.user.username)
        return render(request, "CodeTutor/student_list.html", context={
            "unhandled_requests": tutor.received_applications.count()
        })


def tutor_list(request):
    if (request.method == "GET"):
        return render(request, "CodeTutor/tutor_list.html")


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


@login_required
def load_tutor_profiles(request):
    if (request.method == "GET"):
        # Get start and end profiles
        start = int(request.GET.get('start') or 0)
        end = int(request.GET.get('end') or (start + 9))

        # Generate list of profiles
        data = []
        for i in range(start, end + 1):
            try:
                # Try to get 10 profiles at a time
                data.append(Tutor.objects.all()[i].serialize())
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


@login_required
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
        return HttpResponseRedirect(reverse('success', args=['tutor']))


@login_required
def hire_tutor(request, tutor_username):
    if (request.method == "GET"):
        return render(request, 'CodeTutor/hire_tutor.html', context={
            'tutor': Tutor.objects.get(username=tutor_username),
            # I would use the HiringApplication modelForm but unfortunately the required subjects field is specific for each tutor
            # i.e: That field should only display subjects that the Tutor teaches, hence cannot use a generic modelForm.
        })
    elif (request.method == "POST"):
        # Get information from the form
        information = request.POST

        selected_subject = information.get('selected_subject')
        offered_rates = information.get('offered_rates')

        hiring_application = HiringApplication(subject=Subject.objects.get(subject_name=selected_subject),
                                               offered_rates=offered_rates,
                                               tutor=Tutor.objects.get(username=tutor_username),
                                               student=Student.objects.get(username=request.user.username)
                                               )

        hiring_application.save()

        messages.success(request, "Your application has been received successfully.")
        return HttpResponseRedirect(reverse('success', args=['student']))


@login_required
def my_tutors(request):
    if (request.method == "GET"):
        # Want to get the list of Tutors related to this Student
        tutors = Student.objects.get(username=request.user.username).tutors.all()
        return render(request, 'CodeTutor/my_tutors.html', context={
            "tutors": tutors
        })


# Called when a Student evaluates a Tutor
@login_required
def evaluate(request, tutor_username):
    if (request.method == "GET"):
        return render(request, 'CodeTutor/evaluate.html', context={
            "username": tutor_username,
        })
    elif (request.method == "POST"):
        received_information = request.POST
        tutor = Tutor.objects.get(username=tutor_username)
        student = Student.objects.get(username=request.user.username)
        if (student not in tutor.evaluators.all()):
            # Want to get the values of the ratings the student submitted
            q1_rating = int(received_information.get('q1'))
            q2_rating = int(received_information.get('q2'))
            q3_rating = int(received_information.get('q3'))
            q4_rating = int(received_information.get('q4'))
            q5_rating = int(received_information.get('q5'))

            # Compute the aggregated tutor_score
            aggregate_score = round((q1_rating + q2_rating + q3_rating + q4_rating + q5_rating) / 5, 2)

            # Update the tutor_score based on student's ratings
            Tutor.objects.filter(username=tutor_username).update(tutor_score=round((float(tutor.tutor_score) + aggregate_score) / 2, 2))

            # Update the list of evaluators (students) that the Tutor has received (prevent repeated evaluations)
            tutor.evaluators.add(student)

            messages.success(request, "Your evaluation form has been successfully received.")
            return HttpResponseRedirect(reverse('success', args=['student']))

        # Meaning, this student has already evaluated this tutor at least once
        else:
            messages.success(request, "You have already evaluated this Tutor once.")
            return HttpResponseRedirect(reverse('success', args=['student']))


@login_required
def logout_function(request):
    logout(request)
    return HttpResponseRedirect(reverse("entry"))


def work_in_progress(request):
    return render(request, 'CodeTutor/work_in_progress.html')


@login_required
def success(request, user_type):
    # Note that the success page is shared between tutor and student
    # Hence, the back button should make the correct redirect
    # is_tutor is context
    is_tutor = False
    if (user_type == 'tutor'):
        is_tutor = True
    elif (user_type == 'student'):
        is_tutor = False

    return render(request, 'CodeTutor/success.html', context={
        "is_tutor": is_tutor
    })


@login_required
def received_hiring_requests(request):
    if (request.method == 'GET'):
        tutor = Tutor.objects.get(username=request.user.username)
        hiring_requests = tutor.received_applications.all() # These are the HiringApplication objects
        return render(request, "CodeTutor/received_hiring_requests.html", context={
            "requests": hiring_requests
        })


# If a request is accepted, handle it appropriately
@login_required
def accept(request, type_of_application, application_id):
    if (request.method == 'GET'):
        if (type_of_application == "hiring_application"):
            this_application = HiringApplication.objects.get(id=application_id)

            # If Tutor accepts Student's application, add Student to the list of Students this Tutor has
            this_application.tutor.students.add(this_application.student)
            this_application.tutor.students_taught += 1

            # Get rid of this application
            this_application.delete()

            messages.success(request, "Please check your Profile to view more information about your new student!")
            return HttpResponseRedirect(reverse('success', args=['tutor']))


# If a request is rejected, handle it appropriately
@login_required
def reject(request, type_of_application, application_id):
    if (request.method == 'GET'):
        if (type_of_application == "hiring_application"):
            this_application = HiringApplication.objects.get(id=application_id)

            # Since Tutor has rejected this Student's application, nothing to be done but delete application
            # Get rid of this application
            this_application.delete()

            messages.success(request, "This request has been successfully rejected.")
            return HttpResponseRedirect(reverse('success', args=['tutor']))









