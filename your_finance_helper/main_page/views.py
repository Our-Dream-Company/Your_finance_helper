from django.http import request
from django.shortcuts import render
from .models import GeneralTable
from django.db.models import Sum
from django.views.generic import View, CreateView
from django.urls import reverse_lazy
from .forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameOperationForm
from reports.forms import DateWidgetForm
from .split_queryset import split_queryset
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        data = {'start_date': DateWidgetForm.declared_fields['start_date'].initial,
                'end_date': DateWidgetForm.declared_fields['end_date'].initial}
        form = DateWidgetForm(request.GET or data)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            in_dict_section, in_dict_category, in_dict_name, in_sum_all = split_queryset(
                GeneralTable.objects.filter(
                    id_user=request.user).filter(
                    enabled=False).filter(
                    date__range=[start_date, end_date]).filter(
                    type_of_transaction='IN').values(
                        'id_section__id',
                        'id_section__section',
                        'id_category__id',
                        'id_category__category',
                        'id_category__to_section',
                        'id_name__name_operation',
                        'id_name__to_category').annotate(
                            sum=Sum('sum_money')).order_by(
                                'id_section'))
            out_dict_section, out_dict_category, out_dict_name, out_sum_all = split_queryset(
                GeneralTable.objects.filter(
                    id_user=request.user).filter(
                    enabled=False).filter(
                    date__range=[start_date, end_date]
                ).filter(
                    type_of_transaction='OUT').values(
                        'id_section__id',
                        'id_section__section',
                        'id_category__id',
                        'id_category__category',
                        'id_category__to_section',
                        'id_name__name_operation',
                        'id_name__to_category').annotate(
                            sum=Sum('sum_money')).order_by(
                                'id_section'))
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


class AddIncomeView(LoginRequiredMixin, CreateView):
    form_class = AddIncomeForm
    template_name = 'main_page/add_income.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.instance.id_user = self.request.user
        return super().form_valid(form)


class AddOutcomeView(LoginRequiredMixin, CreateView):
    form_class = AddOutcomeForm
    template_name = 'main_page/add_outcome.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.instance.id_user = self.request.user
        return super().form_valid(form)


class AddNewSectionView(LoginRequiredMixin, CreateView):
    form_class = AddNewSectionForm
    template_name = 'main_page/add_new_section.html'
    success_url = reverse_lazy('add_new_section')

    def form_valid(self, form):
        form.instance.id_user_from_section = self.request.user
        return super().form_valid(form)


class AddNewCategoryView(LoginRequiredMixin, CreateView):
    form_class = AddNewCategoryForm
    template_name = 'main_page/add_new_category.html'
    success_url = reverse_lazy('add_new_category')

    def form_valid(self, form):
        form.instance.id_user_from_category = self.request.user
        return super().form_valid(form)


class AddNewNameOperationView(LoginRequiredMixin, CreateView):
    form_class = AddNewNameOperationForm
    template_name = 'main_page/add_new_name_operation.html'
    success_url = reverse_lazy('add_new_name_operation')

    def form_valid(self, form):
        form.instance.id_user_from_name_operation = self.request.user
        return super().form_valid(form)
