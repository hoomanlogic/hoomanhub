from django import forms
from .models import Action, Flow, Phase, Tag


class ActionForm(forms.ModelForm):
    tags = forms.CharField(max_length=500, required=False)
    target = forms.CharField(max_length=100, label='Add Target', required=False)

    class Meta:
        model = Action
        fields = ['name', 'status']
        labels = {
            'name': 'Action',
        }


class ActionUpdateForm(forms.ModelForm):
    tags = forms.CharField(max_length=500, required=False)
    target = forms.CharField(max_length=100, label='Add Target', required=False)

    class Meta:
        model = Action
        fields = ['name', 'status', 'archived_on']
        labels = {
            'name': 'Action',
        }


class FlowForm(forms.ModelForm):
    class Meta:
        model = Flow


class PhaseForm(forms.ModelForm):
    class Meta:
        model = Phase