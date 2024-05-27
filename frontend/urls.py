
from django.urls import path
from frontend.views import index

urlpatterns = [
    path('', index),
    path('profile/<str:code>',index),
    path('create',index)
]