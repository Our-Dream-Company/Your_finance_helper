from django.shortcuts import render
from main_page.models import *
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView, UpdateView
from .forms import *


class ReportsButtonsView(View):
    def get(self, request):
        return render(request, 'reports/reports.html')


class DetailedCurrentFinancialResultsView(ListView):
    def get(self, request):
        income_all = GeneralTable.objects.order_by('date').filter(
            type_of_transaction='IN').filter(enabled=False)
        outcome_all = GeneralTable.objects.order_by('date').filter(
            type_of_transaction='OUT').filter(enabled=False)
        return render(request, 'reports/detailed_current_financial_results.html', {'income_all': income_all, 'outcome_all': outcome_all})


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
