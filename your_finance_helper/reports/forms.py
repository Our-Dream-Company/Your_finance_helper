from django import forms
from django.db.models import fields
from django.forms import formsets, widgets
from main_page.models import GeneralTable
from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select
from django.forms.formsets import formset_factory
from django.utils import timezone

YEAR_CHOICES = tuple([i for i in range(2010, 2041)])


class TransactionUpdateForm(ModelForm):
    class Meta:
        model = GeneralTable
        exclude = ['enabled']


class TransactionDeleteForm(ModelForm):
    class Meta:
        model = GeneralTable
        fields = ['enabled']


class DateWidgetForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEAR_CHOICES), initial=timezone.now())
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEAR_CHOICES), initial=timezone.now())
