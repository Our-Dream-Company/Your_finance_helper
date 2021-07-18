from django.shortcuts import render
from main_page.models import *
from django.views.generic import View


class ReportsButtonsView(View):
    def get(self, request):
        return render(request, 'reports/reports.html')


class DetailedCurrentFinancialResultsView(View):
    def get(self, request):
        income_all = GeneralTable.objects.values('id_section__section', 'id_category__category', 'id_name__name', 'sum_money',
                                                 'currency', 'date', 'comment').order_by('date').filter(type_of_transaction='IN').filter(enabled=False)
        outcome_all = GeneralTable.objects.values('id_section__section', 'id_category__category', 'id_name__name', 'sum_money',
                                                  'currency', 'date', 'comment').order_by('date').filter(type_of_transaction='OUT').filter(enabled=False)
        return render(request, 'reports/detailed_current_financial_results.html', {'income_all': income_all, 'outcome_all': outcome_all})
