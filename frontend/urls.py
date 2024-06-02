
from django.urls import path
from frontend.views import index

urlpatterns = [
    path('', index),
    path('profile/<str:code>',index),

    path('sign-in',index),
    path('sign-up',index),
    path('update/<str:code>',index),

    path('profile-tutor/<str:code>',index),
    path('sign-in-tutor',index),
    path('sign-up-tutor',index),
    path('update-tutor/<str:code>',index),

]