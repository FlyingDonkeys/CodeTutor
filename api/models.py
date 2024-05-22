from django.db import models
import string
import random
import uuid 


class Room(models.Model):
    dummy = models.CharField(max_length=8, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(null = False, max_length=10, default= uuid.uuid4().hex[:6].upper(), unique=True)
