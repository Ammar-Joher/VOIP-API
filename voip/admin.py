from django.contrib import admin

# Register your models here.
from .models import voip_user

admin.site.register(voip_user)