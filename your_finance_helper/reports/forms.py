from django.db.models import fields
from django.forms import formsets, widgets
from main_page.models import *
from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select
from django.forms.formsets import formset_factory


class TransactionUpdateForm(ModelForm):
    class Meta:
        model = GeneralTable
        exclude = ['enabled']


class TransactionDeleteForm(ModelForm):
    class Meta:
        model = GeneralTable
        fields = ['enabled']
