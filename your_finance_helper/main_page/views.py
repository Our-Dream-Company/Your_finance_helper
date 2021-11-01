from django.shortcuts import render
from .models import GeneralTable
from django.db.models import Sum
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from .forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameForm
from reports.forms import DateWidgetForm
from datetime import datetime
from .split_queryset import split_queryset


class IndexView(View):
    def get(self, request):
        in_dict_section, in_dict_category, in_dict_name, in_sum_all = split_queryset(
            GeneralTable.objects.filter(
                date__range=[datetime.now().replace(day=1).date(),
                             datetime.now().date()]).filter(
                type_of_transaction='IN').values(
                    'id_section__id',
                    'id_section__section',
                    'id_category__id',
                    'id_category__category',
                    'id_category__to_section',
                    'id_name__name',
                    'id_name__to_category').annotate(
                        sum=Sum('sum_money')).order_by(
                            'id_section'))
        out_dict_section, out_dict_category, out_dict_name, out_sum_all = split_queryset(
            GeneralTable.objects.filter(
                date__range=[datetime.now().replace(day=1).date(),
                             datetime.now().date()]
            ).filter(
                type_of_transaction='OUT').values(
                    'id_section__id',
                    'id_section__section',
                    'id_category__id',
                    'id_category__category',
                    'id_category__to_section',
                    'id_name__name',
                    'id_name__to_category').annotate(
                        sum=Sum('sum_money')).order_by(
                            'id_section'))
        form = DateWidgetForm
        return render(request, 'main_page/index.html', {
            'in_dict_section': in_dict_section,
            'in_dict_category': in_dict_category,
            'in_dict_name': in_dict_name,
            'in_sum_all': in_sum_all,
            'out_dict_section': out_dict_section,
            'out_dict_category': out_dict_category,
            'out_dict_name': out_dict_name,
            'out_sum_all': out_sum_all,
            'form': form
        })


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


class AnotherMainPeriod(View):
    def get(self, request):
        if request.method == 'GET':
            form = DateWidgetForm(request.GET)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
            in_dict_section, in_dict_category, in_dict_name, in_sum_all = split_queryset(
                GeneralTable.objects.filter(
                    date__range=[start_date, end_date]
                ).filter(
                    type_of_transaction='IN').values(
                    'id_section__id',
                    'id_section__section',
                    'id_category__id',
                    'id_category__category',
                    'id_category__to_section',
                    'id_name__name',
                    'id_name__to_category').annotate(
                        sum=Sum('sum_money')).order_by(
                            'id_section'))
        out_dict_section, out_dict_category, out_dict_name, out_sum_all = split_queryset(
            GeneralTable.objects.filter(
                date__range=[start_date, end_date]
            ).filter(
                type_of_transaction='OUT').values(
                    'id_section__id',
                    'id_section__section',
                    'id_category__id',
                    'id_category__category',
                    'id_category__to_section',
                    'id_name__name',
                    'id_name__to_category').annotate(
                        sum=Sum('sum_money')).order_by(
                            'id_section'))
        return render(request, 'main_page/another_main_period.html', {
            'in_dict_section': in_dict_section,
            'in_dict_category': in_dict_category,
            'in_dict_name': in_dict_name,
            'in_sum_all': in_sum_all,
            'out_dict_section': out_dict_section,
            'out_dict_category': out_dict_category,
            'out_dict_name': out_dict_name,
            'out_sum_all': out_sum_all
        })
