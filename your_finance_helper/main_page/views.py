from django.shortcuts import render
from .models import GeneralTable, Section
from django.db.models import Sum


def index(request):
    in_data = GeneralTable.objects.filter(
        type_of_transaction='IN').filter(enabled=False).order_by('date')
    out_data = GeneralTable.objects.filter(
        type_of_transaction='OUT').filter(enabled=False).order_by('date')
    out_id = out_data.all().values('id')
    out_section = out_data.all().values(
        'd_section__section').order_by('d_section__section').distinct()
    print(out_section)
    in_sum = in_data.aggregate(in_money=Sum('sum_money'))
    out_sum = out_data.aggregate(out_money=Sum('sum_money'))
    return render(request, 'main_page/index.html', {'in_data': in_data, 'out_data': out_data, 'in_sum': in_sum, 'out_sum': out_sum, 'out_section': out_section})


def add_income(request):
    return render(request, 'main_page/add_income.html')


def add_outcome(request):
    return render(request, 'main_page/add_outcome.html')
