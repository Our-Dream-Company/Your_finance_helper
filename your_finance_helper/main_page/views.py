from django.shortcuts import render
from .models import Category, GeneralTable, Section
from django.db.models import Sum
from django.views.generic import View, CreateView


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


class AddIncome(CreateView):
    form_class = AddPostForm


# def add_income(request):
#     return render(request, 'main_page/add_income.html')


def add_outcome(request):
    return render(request, 'main_page/add_outcome.html')
