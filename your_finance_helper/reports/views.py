from django.shortcuts import render
from main_page.models import GeneralTable
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, UpdateView
from .forms import DateWidgetForm, TransactionUpdateForm, TransactionDeleteForm, DateWidgetForm


class ReportsButtonsView(View):
    def get(self, request):
        return render(request, 'reports/reports.html')


class DetailedCurrentFinancialResultsView(View):
    def get(self, request):
        data = {'start_date': DateWidgetForm.declared_fields['start_date'].initial,
                'end_date': DateWidgetForm.declared_fields['end_date'].initial}
        form = DateWidgetForm(request.GET or data)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            income_all = GeneralTable.objects.order_by('date').filter(
                date__range=[start_date, end_date]).filter(
                type_of_transaction='IN').filter(
                enabled=False)
            outcome_all = GeneralTable.objects.order_by('date').filter(
                date__range=[start_date, end_date]).filter(
                type_of_transaction='OUT').filter(
                enabled=False)
            return render(request, 'reports/detailed_current_financial_results.html', {
                'start_date': start_date,
                'end_date': end_date,
                'income_all': income_all,
                'outcome_all': outcome_all,
                'form': form
            })


class TransactionView(DetailView):
    model = GeneralTable
    template_name = 'reports/transaction_view.html'
    context_object_name = 'transaction'


class TransactionUpdateView(UpdateView):
    model = GeneralTable
    template_name = 'reports/transaction_update.html'
    form_class = TransactionUpdateForm
    context_object_name = 'transaction_form'
    success_url = reverse_lazy('detailed_current_financial_results')


class TransactionDeleteView(UpdateView):
    model = GeneralTable
    template_name = 'reports/transaction_delete.html'
    form_class = TransactionDeleteForm
    context_object_name = 'transaction_d_form'
    success_url = reverse_lazy('detailed_current_financial_results')
