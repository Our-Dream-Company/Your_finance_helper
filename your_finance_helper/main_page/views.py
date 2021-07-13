from django.shortcuts import render
from .models import *
from django.db.models import Sum
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from .forms import *


class IndexView(View):
    def get(self, request):
        in_section = GeneralTable.objects.values(
            'id_section__section', 'id_section__id').annotate(sum=Sum('sum_money')).filter(type_of_transaction='IN').filter(enabled=False)
        in_category = GeneralTable.objects.values(
            'id_category__id', 'id_category__category', 'id_category__to_section').distinct().filter(id_category__isnull=False).filter(type_of_transaction='IN').filter(enabled=False)
        in_name = GeneralTable.objects.values(
            'id_name__name', 'id_name__to_category').annotate(sum=Sum('sum_money')).filter(id_name__isnull=False).filter(type_of_transaction='IN').filter(enabled=False)
        in_all_sum = GeneralTable.objects.filter(type_of_transaction='IN').filter(
            enabled=False).aggregate(in_money=Sum('sum_money'))
        out_section = GeneralTable.objects.values(
            'id_section__section', 'id_section__id').annotate(sum=Sum('sum_money')).filter(type_of_transaction='OUT').filter(enabled=False)
        out_category = GeneralTable.objects.values(
            'id_category__id', 'id_category__category', 'id_category__to_section').distinct().filter(id_category__isnull=False).filter(type_of_transaction='OUT').filter(enabled=False)
        out_name = GeneralTable.objects.values(
            'id_name__name', 'id_name__to_category').annotate(sum=Sum('sum_money')).filter(id_name__isnull=False).filter(type_of_transaction='OUT').filter(enabled=False)
        out_all_sum = GeneralTable.objects.filter(type_of_transaction='OUT').filter(
            enabled=False).aggregate(out_money=Sum('sum_money'))
        return render(request, 'main_page/index.html', {'in_section': in_section, 'in_category': in_category, 'in_name': in_name, 'out_section': out_section, 'out_category': out_category, 'out_name': out_name, 'in_all_sum': in_all_sum, 'out_all_sum': out_all_sum})


class AddIncomeView(CreateView):
    form_class = AddIncomeForm
    template_name = 'main_page/add_income.html'
    success_url = reverse_lazy('main_page')


class AddOutcomeView(CreateView):
    form_class = AddOutcomeForm
    template_name = 'main_page/add_outcome.html'
    success_url = reverse_lazy('main_page')


class AddNewSectionView(CreateView):
    form_class = AddNewSectionForm
    template_name = 'main_page/add_new_section.html'
    success_url = reverse_lazy('add_new_section')


class AddNewCategoryView(CreateView):
    form_class = AddNewCategoryForm
    template_name = 'main_page/add_new_category.html'
    success_url = reverse_lazy('add_new_category')


class AddNewNameView(CreateView):
    form_class = AddNewNameForm
    template_name = 'main_page/add_new_name.html'
    success_url = reverse_lazy('add_new_name')
