from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import User, Tv_Episode, Tv_Series, Movie, Event

admin.site.register((User, Tv_Episode, Tv_Series, Movie, Event))
