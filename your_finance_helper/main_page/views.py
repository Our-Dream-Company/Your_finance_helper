from django.shortcuts import render
from .models import Category, GeneralTable, Section
from django.db.models import Sum
from django.views.generic import View


class IndexView(View):
    def get(self, request):
        data = GeneralTable.objects.values('id_section__section', 'id_section__id', 'id_category').order_by(
            'id_section').filter(type_of_transaction='OUT').distinct()
        category = Category.objects.values('id', 'category')
        return render(request, 'main_page/index.html', {'data': data, 'category': category})

# def index(request):
#    in_data = GeneralTable.objects.filter(
#        type_of_transaction='IN').filter(enabled=False).order_by('date')
#    out_data = GeneralTable.objects.filter(type_of_transaction='OUT').filter(enabled=False).order_by('date')
#    out_id = out_data.all().values('id')
#    out_section = out_data.all().values(
#        'id_section__section').order_by('id_section__section').distinct()
#    print(out_section)
#    in_sum = in_data.aggregate(in_money=Sum('sum_money'))
#    out_sum = out_data.aggregate(out_money=Sum('sum_money'))
#    return render(request, 'main_page/index.html', {'in_data': in_data, 'out_data': out_data, 'in_sum': in_sum, 'out_sum': out_sum, 'out_section': out_section})


def add_income(request):
    return render(request, 'main_page/add_income.html')


def add_outcome(request):
    return render(request, 'main_page/add_outcome.html')
