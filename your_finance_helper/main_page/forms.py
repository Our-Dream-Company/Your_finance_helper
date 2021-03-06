from django.http import request, response
from .models import Section, Category, NameOperation, GeneralTable
from django.forms import ModelForm, TextInput, DateInput, NumberInput, Select


class AddIncomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.type_of_transaction = 'IN'
        kwargs['instance'] = self.instance
        super(AddIncomeForm, self).__init__(*args, **kwargs)
        self.fields['id_section'].empty_label = 'Choose a Section'
        self.fields['id_category'].empty_label = 'Choose a Category'
        self.fields['id_name'].empty_label = 'Choose a Name Operation'

    class Meta:
        model = GeneralTable
        exclude = ['type_of_transaction', 'enabled', 'id_user']
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


class AddOutcomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.type_of_transaction = 'OUT'
        kwargs['instance'] = self.instance
        super(AddOutcomeForm, self).__init__(*args, **kwargs)
        self.fields['id_section'].empty_label = 'Choose a Section'
        self.fields['id_category'].empty_label = 'Choose a Category'
        self.fields['id_name'].empty_label = 'Choose a Name Operation'

    class Meta:
        model = GeneralTable
        exclude = ['type_of_transaction', 'enabled', 'id_user']
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


class AddNewSectionForm(ModelForm):
    class Meta:
        model = Section
        exclude = ['enabled_section', 'id_user_from_section']
        widgets = {
            'section': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Section'
            })
        }


class AddNewCategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_section'].empty_label = 'Choose a Section'

    class Meta:
        model = Category
        exclude = ['enabled_category', 'id_user_from_category']
        widgets = {
            'category': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category'
            }),
            'to_section': Select(attrs={
                'class': 'form-control',
            })
        }


class AddNewNameOperationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_category'].empty_label = 'Choose a Category'

    class Meta:
        model = NameOperation
        exclude = ['enabled_name', 'id_user_from_name_operation']
        widgets = {
            'name_operation': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name Operation'
            }),
            'to_category': Select(attrs={
                'class': 'form-control',
            })
        }
