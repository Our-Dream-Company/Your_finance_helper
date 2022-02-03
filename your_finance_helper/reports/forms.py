from datetime import datetime
from django import forms
from main_page.models import GeneralTable
from django.forms import ModelForm, Select, NumberInput, DateInput, TextInput

YEAR_CHOICES = tuple(i for i in range(2010, 2041))


class TransactionUpdateForm(ModelForm):
    class Meta:
        model = GeneralTable
        exclude = ['enabled', 'id_user']
        widgets = {
            'type_of_transaction': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Type of transaction'
            }),
            'id_section': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Section'
            }),
            'id_category': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Category'
            }),
            'id_name': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Name Operation:'
            }),
            'sum_money': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount'
            }),
            'currency': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Currency'
            }),
            'date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Date'
            }),
            'comment': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comment'
            })
        }


class TransactionDeleteForm(ModelForm):
    class Meta:
        model = GeneralTable
        fields = ['enabled']


class DateWidgetForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEAR_CHOICES), initial=datetime.now().replace(day=1).date())
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEAR_CHOICES), initial=datetime.now().date())
