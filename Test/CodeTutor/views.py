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
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import json

@login_required
def profile(request):
    return render(request, "CodeTutor/profile.html")


@login_required
def load_user_profile(request):
    if request.method == "GET":
        user = None
        query_set = Student.objects.all().filter(username=request.user.username)
        if query_set.exists():
            user = query_set.first()
            picture = 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
            print(user.profile_picture)
            try:
                picture = user.profile_picture.url
            except:
                pass
            context = {
                'google_api_key': settings.GOOGLE_API_KEY,
                'is_student': True,
                'user': {
                    'username': user.username,
                    'id': user.id,
                    'location': user.location,
                    'postal_code': user.postal_code,
                    'finding_tutor':user.is_finding_tutor,
                    'profile_picture_url': picture
                }
            }
            return JsonResponse(context, safe=False)
        else:
            query_set = Tutor.objects.all().filter(username=request.user.username)
            user = query_set[0]
            picture = 'https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg'
            try:
                picture = user.profile_picture.url
            except:
                pass

        context = {
            'google_api_key': settings.GOOGLE_API_KEY,
            'is_student': False,
            'user': {
                'username': user.username,
                'id': user.id,
                'description': user.tutor_description,
                'profile_picture_url': picture
            }
        }
        return JsonResponse(context, safe=False)


# STRIPE API

#Enter the page 
@login_required(login_url='login')
def subsribe(request):
    if request.method == "POST":
        return render(request, 'CodeTutor/product_page.html')
    return render(request, 'CodeTutor/product_page.html')

@login_required(login_url='login')
def product_page(request, kwarg):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    if request.method == 'POST':
        print(kwarg)
        PRODUCT_PRICE = None
        #Assign a product according to option chosen
        if kwarg == '0':
            print("case0")
            PRODUCT_PRICE = settings.PRODUCT_WEEKLY
        elif kwarg == '1':
            print("case1")
            PRODUCT_PRICE = settings.PRODUCT_MONTHLY
        else:   
            print("case2")
            PRODUCT_PRICE = settings.PRODUCT_YEARLY

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': PRODUCT_PRICE, 
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}&kwarg={kwarg}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    return reverse('subscribe')


# Goes here if successful,works only with real web address
## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get('session_id', None)
    print(checkout_session_id)
    kwarg = request.GET.get('kwarg',None)
    Timer = date.today()
    if kwarg == 0:
        Timer += relativedelta(weeks=+1)
    elif kwarg == 1:
        Timer += relativedelta(months=+1)
    else:
        Timer +=  relativedelta(months=+12)
    #session = stripe.checkout.Session.retrieve(checkout_session_id)
    #customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user.id
    print(f"user_id {user_id}")
    user = Tutor.objects.get(id = user_id)
    #ClassModel.(object_id)
    print(f"user {user}")
    set = UserPayment.objects.filter(app_user=user)
    user_payment = None
    if not set.exists():
        user_payment =  UserPayment.objects.create(app_user = user)
    else:
        user_payment = set[0]
    print(f"user_payment {user_payment}")
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.count_down = Timer
    user_payment.save()
    return HttpResponseRedirect(reverse("student_list"))


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

    elif (request.method == 'GET' and request.user.is_authenticated):
        # First 2 conditionals mainly handle users who sign up using classic Django
        if (Tutor.objects.filter(username=request.user.username)):
            return HttpResponseRedirect(reverse("student_list"))
        elif (Student.objects.filter(username=request.user.username)):
            return HttpResponseRedirect(reverse("tutor_list"))

        # Only applicable for Google related accounts, when there is a related CommonUser (Google creates CommonUser
        # instead of a Tutor or Student profile by default)
        elif (CommonUser.objects.get(username=request.user.username)):
            current_user = CommonUser.objects.get(username=request.user.username)
            if (current_user.related_tutor.count() == 1):
                logout(request)
                login(request, current_user.related_tutor.first(), backend="django.contrib.auth.backends.ModelBackend")
                return HttpResponseRedirect(reverse("student_list"))
            elif (current_user.related_student.count() == 1):
                logout(request)
                login(request, current_user.related_student.first(), backend="django.contrib.auth.backends.ModelBackend")
                return HttpResponseRedirect(reverse("tutor_list"))
            else:
                # When Google does sign in, default User is created, have to either create Tutor or Student account afterwards
                # This will only run if there is no existing account associated with this user id.
                return HttpResponseRedirect(reverse("create_profile"))

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


def create_profile(request):
    if (request.method == "GET"):

        # Want to pre-populate fields using Google provided info
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }

        # Instantiate forms with initial data
        tutor_form = TutorRegistrationForm(initial=initial_data)
        student_form = StudentRegistrationForm(initial=initial_data)

        # Disable fields
        for field in ['first_name', 'last_name', 'email']:
            tutor_form.fields[field].widget.attrs['readonly'] = True
            student_form.fields[field].widget.attrs['readonly'] = True

        return render(request, "CodeTutor/create_profile.html", context={
            "tutor_registration_form": tutor_form,
            "student_registration_form": student_form
        })

    # Need delete existing User and replace with correct user class
    elif (request.method == 'POST'):
        if ("student" in request.POST):
            student_registration_form = StudentRegistrationForm(request.POST, request.FILES)
            if (student_registration_form.is_valid()):
                return register_student_google(request, student_registration_form)
            else:
                return render(request, 'CodeTutor/create_profile.html', {
                    "student_registration_form": student_registration_form,
                    "tutor_registration_form": TutorRegistrationForm,
                    "student_error": True,
                    "tutor_error": False
                })
        elif ("tutor" in request.POST):
            tutor_registration_form = TutorRegistrationForm(request.POST, request.FILES)
            if (tutor_registration_form.is_valid()):
                return register_tutor_google(request, tutor_registration_form)
            else:
                return render(request, 'CodeTutor/create_profile.html', {
                    "tutor_registration_form": tutor_registration_form,
                    "student_registration_form": StudentRegistrationForm,
                    "tutor_error": True,
                    "student_error": False
                })


def register_student(request, student_registration_form):
    new_student = Student.objects.create(
        username=student_registration_form.cleaned_data['username'],
        first_name=student_registration_form.cleaned_data['first_name'],
        last_name=student_registration_form.cleaned_data['last_name'],
        email=student_registration_form.cleaned_data['email'],
        mobile_number=student_registration_form.cleaned_data['mobile_number'],
        location=student_registration_form.cleaned_data['location'],
        profile_picture=student_registration_form.cleaned_data['profile_picture'],
        offered_rate = student_registration_form.cleaned_data['offered_rate'],
        postal_code = student_registration_form.cleaned_data['postal_code'],
        related_user=None
    )

    password = student_registration_form.cleaned_data['password']
    subjects_required = student_registration_form.cleaned_data['subjects_required']
    # Assign the many-to-many field after making the student object
    new_student.subjects_required.set(subjects_required)
    new_student.set_password(password)
    new_student.save()

    # Use Django messages framework to pass context to the html
    messages.success(request, "You have successfully registered your student profile. Please proceed to login.")
    return HttpResponseRedirect(reverse("entry"))


def register_student_google(request, student_registration_form):
    new_student = Student.objects.create(
        username=student_registration_form.cleaned_data['username'],
        first_name=student_registration_form.cleaned_data['first_name'],
        last_name=student_registration_form.cleaned_data['last_name'],
        email=student_registration_form.cleaned_data['email'],
        mobile_number=student_registration_form.cleaned_data['mobile_number'],
        location=student_registration_form.cleaned_data['location'],
        profile_picture=student_registration_form.cleaned_data['profile_picture'],
        offered_rate = student_registration_form.cleaned_data['offered_rate'],
        related_user = CommonUser.objects.get(username=request.user.username)
        postal_code = student_registration_form.cleaned_data['postal_code']
    )

    password = student_registration_form.cleaned_data['password']
    subjects_required = student_registration_form.cleaned_data['subjects_required']
    # Assign the many-to-many field after making the student object
    new_student.subjects_required.set(subjects_required)
    new_student.set_password(password)
    new_student.save()

    # Use Django messages framework to pass context to the html
    messages.success(request, "You have successfully registered your student profile. Please proceed to login.")
    return HttpResponseRedirect(reverse("entry"))


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
        profile_picture=tutor_registration_form.cleaned_data['profile_picture'],
        related_user=None
    )

    password = tutor_registration_form.cleaned_data['password']
    subjects_taught = tutor_registration_form.cleaned_data['subjects_taught']
    # Assign the many-to-many field after making the student object
    new_tutor.subjects_taught.set(subjects_taught)
    new_tutor.set_password(password)
    new_tutor.save()

    return HttpResponseRedirect(reverse("entry"))


def register_tutor_google(request, tutor_registration_form):
    print("in register tutor view")
    new_tutor = Tutor.objects.create(
        username=tutor_registration_form.cleaned_data['username'],
        first_name=tutor_registration_form.cleaned_data['first_name'],
        last_name=tutor_registration_form.cleaned_data['last_name'],
        email=tutor_registration_form.cleaned_data['email'],
        mobile_number=tutor_registration_form.cleaned_data['mobile_number'],
        tutor_qualification=tutor_registration_form.cleaned_data['tutor_qualification'],
        hourly_rate=tutor_registration_form.cleaned_data['hourly_rate'],
        tutor_description=tutor_registration_form.cleaned_data['tutor_description'],
        profile_picture=tutor_registration_form.cleaned_data['profile_picture'],
        related_user=CommonUser.objects.get(username=request.user.username)
    )

    password = tutor_registration_form.cleaned_data['password']
    subjects_taught = tutor_registration_form.cleaned_data['subjects_taught']
    # Assign the many-to-many field after making the tutor object
    new_tutor.subjects_taught.set(subjects_taught)
    new_tutor.set_password(password)
    new_tutor.save()

    return HttpResponseRedirect(reverse("entry"))




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
            querySet = Tutor.objects.filter(username=username)
            if (querySet.exists()):
                #if subscription has 0 days left, redirect to product page 
                current_tutor = querySet.first()
                user = UserPayment.objects.filter(app_user=current_tutor)
                if(user.exists()):
                    #Only redirect to student page if count down is larger than 0 
                    if user.first().count_down > timezone.now():
                        return HttpResponseRedirect(reverse("student_list"))
                #redirect to product page 
                return HttpResponseRedirect(reverse("subscribe"))
            elif (Student.objects.filter(username=username)):
                return HttpResponseRedirect(reverse("tutor_list"))

            # Otherwise, the user is an admin, but we dont care abt this
            return HttpResponseRedirect(reverse("work_in_progress"))
        else:
            return render(request, "CodeTutor/index.html", {
                "message": "Invalid username and/or password."
            })

def change_active_state(request):
    if (request.method == "POST"):
        #find student first
        queryset = Student.objects.filter(username = request.user.username)
        student = queryset.first()
        print(student.is_finding_tutor)
        if(student.is_finding_tutor):
            student.is_finding_tutor= False
            student.save()
        else:
            student.is_finding_tutor = True
            student.save()
        return HttpResponseRedirect(reverse("profile"))

# Note that only tutors should be able to view this page
@login_required
def student_list(request):
    if (request.method == "GET"):

        #if subscription has 0 days left, redirect to product page 
        #print(request.user.username)
        tutor = Tutor.objects.filter(username=request.user.username)
        user = UserPayment.objects.filter(app_user=tutor.first())
        print(user.first())
        if(user.exists()):
            #Only redirect to student page if count down is larger than 0 
            if user.first().count_down > timezone.now():
                return render(request, "CodeTutor/student_list.html")
                #redirect to product page 
        return HttpResponseRedirect(reverse("subscribe"))


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
        print(Tutor.objects.all()[0].serialize())
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

@login_required
def my_students(request):
    if (request.method == "GET"):
        # Want to get the list of Students related to this Student
        return render(request, 'CodeTutor/my_students.html', context={
            "students": Student.objects.all()
        })
    
@login_required
def data(request):
    if(request.method == "GET"):
        students = Tutor.objects.get(username=request.user.username).students.all()
        serialised_data = []
        for student in students:
            temp = student.serialize()
            del temp["date_joined"]
            serialised_data.append(temp)
        print(serialised_data)
        return JsonResponse(serialised_data, safe=False)
    
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
def received_tutor_requests(request):
    if(request.method == "GET"):
        student = Student.objects.get(username=request.user.username)
        tutor_requests = student.received_applications.all()
        return render(request, "CodeTutor/received_tutor_requests.html", context={
            "requests": tutor_requests
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

# google is great


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
        
        if(type_of_application == "application"):
            this_application = Application.objects.get(id = application_id)
            this_application.student.tutors.add(this_application.tutor)
            this_application.delete()
            messages.success(request, "Please check the `My Tutors` page to view more information about your new tutor!")
            return HttpResponseRedirect(reverse('success', args=['student']))


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
        
        if (type_of_application == "application"):
            this_application = Application.objects.get(id=application_id)

            # Since Tutor has rejected this Student's application, nothing to be done but delete application
            # Get rid of this application
            this_application.delete()

            messages.success(request, "This request has been successfully rejected.")
            return HttpResponseRedirect(reverse('success', args=['student']))









