from django.contrib import admin

from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
app_name = 'users'

admin.site.register(User, UserAdmin)



