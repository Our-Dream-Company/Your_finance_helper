from django.shortcuts import render
from main_page.models import GeneralTable
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView, UpdateView
from .forms import DateWidgetForm, TransactionUpdateForm, TransactionDeleteForm


class ReportsButtonsView(View):
    def get(self, request):
        return render(request, 'reports/reports.html')


class DetailedCurrentFinancialResultsView(ListView):
    def get(self, request):
        income_all = GeneralTable.objects.order_by('date').filter(
            type_of_transaction='IN').filter(enabled=False)
        outcome_all = GeneralTable.objects.order_by('date').filter(
            type_of_transaction='OUT').filter(enabled=False)
        form = DateWidgetForm
        return render(request, 'reports/detailed_current_financial_results.html', {'income_all': income_all, 'outcome_all': outcome_all, 'form': form})


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


class Test(DetailView):
    model = GeneralTable
    template_name = 'reports/test.html'

    def get_context_data(self, **kwargs):
        context = super(Test, self).get_context_data(**kwargs)
        page_alt = GeneralTable.objects.get(id=self.kwargs.get('pk_alt', ''))
        context['page_alt'] = page_alt
        return context
