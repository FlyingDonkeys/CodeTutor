
from django.urls import path
from frontend.views import index

urlpatterns = [

    path('', index),

    path('join', index),

    path('create', index)
    
]