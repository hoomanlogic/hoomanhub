from django import forms
from .models import Action, Flow, Phase, Tag


class ActionForm(forms.ModelForm):
    tags = forms.CharField(max_length=500)

    class Meta:
        model = Action
        fields = ['name']
        labels = {
            'name': 'Action',
        }



class FlowForm(forms.ModelForm):
    class Meta:
        model = Flow


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase