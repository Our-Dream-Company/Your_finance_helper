
from django.forms import formsets
from .models import *
from django.forms import ModelForm
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
