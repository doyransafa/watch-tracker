from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Tv_Episode, Tv_Series, Movie, Event, List

admin.site.register((Tv_Episode, Tv_Series, Movie, Event, List))
