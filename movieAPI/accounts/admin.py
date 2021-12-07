from django.contrib import admin

# Register your models here.
from .models import User, Profile , List

admin.site.register(Profile)
admin.site.register(List)