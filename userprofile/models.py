from django.db import models
from authentication.models import MyUser

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=254)
    nick_name = models.CharField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=494)
    contact = models.CharField(max_length=11)

    def __str__(self):
        return str(self.address)
