from django.db import models

# Create your models here.
class voip_user(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    received_count = models.IntegerField(default=0)
    notes = models.TextField()

    def __str__(self):
        return self.name;