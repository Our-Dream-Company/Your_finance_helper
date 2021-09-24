import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from main_page.models import GeneralTable
from reports.forms import TransactionUpdateForm, TransactionDeleteForm


def test_view_uses_correct_template_reports(client):
    resp = client.get(reverse('reports'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'reports/reports.html')


@pytest.mark.django_db
def test_view_uses_correct_template_detailed_current_financial_results_reports(client):
    resp = client.get(reverse('detailed_current_financial_results'))
    assert resp.status_code == 200
    assertTemplateUsed(
        resp, 'reports/detailed_current_financial_results.html')


@pytest.mark.django_db
def test_view_uses_correct_template_one_transaction_reports(client, published_post_add_income_transaction):
    resp = client.get(reverse('transaction_view', args=[
        GeneralTable.objects.last().id]))
    assert resp.status_code, 200
    assertTemplateUsed(
        resp, 'reports/transaction_view.html')


@pytest.mark.django_db
def test_view_uses_correct_template_transaction_update_reports(client, published_post_add_income_transaction):
    resp = client.get(reverse('transaction_update', args=[
        GeneralTable.objects.last().id]))
    assert resp.status_code == 200
    assertTemplateUsed(
        resp, 'reports/transaction_update.html')


@pytest.mark.django_db
def test_view_uses_correct_template_transaction_delete_reports(client, published_post_add_income_transaction):
    resp = client.get(reverse('transaction_delete', args=[
        GeneralTable.objects.last().id]))
    assert resp.status_code, 200
    assertTemplateUsed(
        resp, 'reports/transaction_delete.html')


@pytest.mark.django_db
def test_correct_form_in_transaction_update_reports(client, published_post_add_income_transaction):
    response = client.get(reverse('transaction_update', args=[
        GeneralTable.objects.last().id]))
    assert isinstance(
        response.context['form'], TransactionUpdateForm)


@pytest.mark.django_db
def test_correct_form_in_transaction_update_reports(client, published_post_add_income_transaction):
    response = client.get(reverse('transaction_delete', args=[
        GeneralTable.objects.last().id]))
    assert isinstance(
        response.context['form'], TransactionDeleteForm)


@pytest.mark.django_db
def test_correct_data_for_template_in_detailed_current_financial_results_reports(client, published_post_add_income_transaction, published_post_add_outcome_transaction):
    response = client.get(reverse('detailed_current_financial_results'))
    assert str(response.context['income_all'][0].type_of_transaction) == 'IN'
    assert str(response.context['income_all'][0].id_section) == 'Работа'
    assert str(response.context['income_all'][0].id_category) == 'Подработка'
    assert str(response.context['income_all'][0].id_name) == 'Клуб'
    assert str(response.context['income_all'][0].sum_money) == '50000.00'
    assert str(response.context['income_all'][0].currency) == 'BYN'
    assert str(response.context['income_all'][0].date) == '2021-06-01'
    assert str(response.context['income_all'][0].comment) == 'ква'
    assert response.context['income_all'][0].enabled == False
    assert str(response.context['outcome_all'][0].type_of_transaction) == 'OUT'
    assert str(response.context['outcome_all'][0].id_section) == 'Мои расходы'
    assert str(response.context['outcome_all'][0].id_category) == 'Аптека'
    assert str(response.context['outcome_all'][0].id_name) == 'Антибиотики'
    assert str(response.context['outcome_all'][0].sum_money) == '-500.00'
    assert str(response.context['outcome_all'][0].currency) == 'BYN'
    assert str(response.context['outcome_all'][0].date) == '2021-06-03'
    assert str(response.context['outcome_all'][0].comment) == 'кря'
    assert response.context['outcome_all'][0].enabled == False


@pytest.mark.django_db
def test_correct_data_for_template_in_one_transaction_reports(client, published_post_add_income_transaction):
    resp = client.get(reverse('transaction_view', args=[
        GeneralTable.objects.last().id]))
    assert resp.context['transaction'].type_of_transaction == 'IN'
    assert str(resp.context['transaction'].id_section) == 'Работа'
    assert str(resp.context['transaction'].id_category) == 'Подработка'
    assert str(resp.context['transaction'].id_name) == 'Клуб'
    assert str(resp.context['transaction'].sum_money) == '50000.00'
    assert str(resp.context['transaction'].currency) == 'BYN'
    assert str(resp.context['transaction'].date) == '2021-06-01'
    assert str(resp.context['transaction'].comment) == 'ква'
    assert resp.context['transaction'].enabled == False


@pytest.mark.django_db
def test_correct_data_for_template_in_transaction_update_reports(client, published_post_add_income_transaction):
    resp = client.get(reverse('transaction_update', args=[
        GeneralTable.objects.last().id]))
    assert resp.context['transaction_form'].type_of_transaction == 'IN'
    assert str(resp.context['transaction_form'].id_section) == 'Работа'
    assert str(resp.context['transaction_form'].id_category) == 'Подработка'
    assert str(resp.context['transaction_form'].id_name) == 'Клуб'
    assert str(resp.context['transaction_form'].sum_money) == '50000.00'
    assert str(resp.context['transaction_form'].currency) == 'BYN'
    assert str(resp.context['transaction_form'].date) == '2021-06-01'
    assert str(resp.context['transaction_form'].comment) == 'ква'
    assert resp.context['transaction_form'].enabled == False


@pytest.mark.django_db
def test_correct_data_for_template_in_transaction_delete_reports(client, published_post_add_income_transaction):
    resp = client.get(reverse('transaction_delete', args=[
        GeneralTable.objects.last().id]))
    assert resp.context['transaction_d_form'].type_of_transaction == 'IN'
    assert str(resp.context['transaction_d_form'].id_section) == 'Работа'
    assert str(resp.context['transaction_d_form'].id_category) == 'Подработка'
    assert str(resp.context['transaction_d_form'].id_name) == 'Клуб'
    assert str(resp.context['transaction_d_form'].sum_money) == '50000.00'
    assert str(resp.context['transaction_d_form'].currency) == 'BYN'
    assert str(resp.context['transaction_d_form'].date) == '2021-06-01'
    assert str(resp.context['transaction_d_form'].comment) == 'ква'
    assert resp.context['transaction_d_form'].enabled == False
