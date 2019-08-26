from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import ForeignKey


class voip_user(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    received_count = models.IntegerField(default=0)
    notes = models.TextField()
    user = ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name;