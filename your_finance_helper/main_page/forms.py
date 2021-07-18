
from django.forms import formsets, widgets
from .models import *
from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select
from django.forms.formsets import formset_factory


class AddIncomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.type_of_transaction = 'IN'
        kwargs['instance'] = self.instance
        super(AddIncomeForm, self).__init__(*args, **kwargs)
        self.fields['id_section'].empty_label = 'Choose a Section'
        self.fields['id_category'].empty_label = 'Choose a Category'
        self.fields['id_name'].empty_label = 'Choose a Name'

    class Meta:
        model = GeneralTable
        exclude = ['type_of_transaction', 'enabled']
        widgets = {
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
                'placeholder': 'Name:'
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


class AddOutcomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.type_of_transaction = 'OUT'
        kwargs['instance'] = self.instance
        super(AddOutcomeForm, self).__init__(*args, **kwargs)
        self.fields['id_section'].empty_label = 'Choose a Section'
        self.fields['id_category'].empty_label = 'Choose a Category'
        self.fields['id_name'].empty_label = 'Choose a Name'

    class Meta:
        model = GeneralTable
        exclude = ['type_of_transaction', 'enabled']
        widgets = {
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
                'placeholder': 'Name:'
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


class AddNewSectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ['enabled_section']


class AddNewCategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['enabled_category']


class AddNewNameForm(ModelForm):
    class Meta:
        model = NameOperation
        exclude = ['enabled_name']
