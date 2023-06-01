from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    email_verify = models.BooleanField(default=False)
    verification_code = models.IntegerField(blank=True, null=True)
