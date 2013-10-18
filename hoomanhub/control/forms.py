from django import forms
from .models import Hooman


class HoomanForm(forms.ModelForm):
    class Meta:
        model = Hooman