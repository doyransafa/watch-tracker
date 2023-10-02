from django import forms
# from django.forms import ModelForm, Form

    

from .models import List


class CreateListForm(forms.ModelForm):
    
    class Meta:
        model = List
        fields = ['name', 'description', 'public']

class UpdateListForm(forms.ModelForm):
    
    class Meta:
        model = List
        fields = ['name', 'description', 'public']


class AddListItemsForm(forms.Form):

    movie_id = forms.IntegerField()
    tv_series_id = forms.IntegerField()
    body = forms.Textarea()