from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# from django.model import Habit

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email']