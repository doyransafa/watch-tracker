from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Follow

admin.site.register((User, Profile, Follow))
