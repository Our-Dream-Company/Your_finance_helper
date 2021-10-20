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
def test_view_uses_correct_template_one_transaction_reports(client, transaction_in):
    resp = client.get(reverse('transaction_view', args=[
        transaction_in.id]))
    assert resp.status_code, 200
    assertTemplateUsed(
        resp, 'reports/transaction_view.html')


@pytest.mark.django_db
def test_view_uses_correct_template_transaction_update_reports(client, transaction_in):
    resp = client.get(reverse('transaction_update', args=[
                      transaction_in.id]))
    assert resp.status_code == 200
    assertTemplateUsed(
        resp, 'reports/transaction_update.html')


@pytest.mark.django_db
def test_view_uses_correct_template_transaction_delete_reports(client, transaction_in):
    resp = client.get(reverse('transaction_delete', args=[
                      transaction_in.id]))
    assert resp.status_code, 200
    assertTemplateUsed(
        resp, 'reports/transaction_delete.html')


@pytest.mark.django_db
def test_correct_form_in_transaction_update_reports(client, transaction_in):
    response = client.get(reverse('transaction_update', args=[
                          transaction_in.id]))
    assert isinstance(
        response.context['form'], TransactionUpdateForm)


@pytest.mark.django_db
def test_correct_form_in_transaction_update_reports(client, transaction_in):
    response = client.get(reverse('transaction_delete', args=[
                          transaction_in.id]))
    assert isinstance(
        response.context['form'], TransactionDeleteForm)


@pytest.mark.django_db
def test_correct_data_for_template_in_detailed_current_financial_results_reports(client, transaction_in, transaction_out):
    response = client.get(reverse('detailed_current_financial_results'))
    assert str(transaction_in.type_of_transaction) == str(
        response.context['income_all'][0].type_of_transaction)
    assert str(transaction_in.id_section) == str(
        response.context['income_all'][0].id_section)
    assert str(transaction_in.id_category) == str(
        response.context['income_all'][0].id_category)
    assert str(transaction_in.id_name) == str(
        response.context['income_all'][0].id_name)
    assert str(transaction_in.sum_money) == str(
        response.context['income_all'][0].sum_money)
    assert str(transaction_in.currency) == str(
        response.context['income_all'][0].currency)
    assert str(transaction_in.date) == str(
        response.context['income_all'][0].date)
    assert str(transaction_in.comment) == str(
        response.context['income_all'][0].comment)
    assert transaction_in.enabled == response.context['income_all'][0].enabled
    assert str(transaction_out.type_of_transaction) == str(
        response.context['outcome_all'][0].type_of_transaction)
    assert str(transaction_out.id_section) == str(
        response.context['outcome_all'][0].id_section)
    assert str(transaction_out.id_category) == str(
        response.context['outcome_all'][0].id_category)
    assert str(transaction_out.id_name) == str(
        response.context['outcome_all'][0].id_name)
    assert str(transaction_out.sum_money) == str(
        response.context['outcome_all'][0].sum_money)
    assert str(transaction_out.currency) == str(
        response.context['outcome_all'][0].currency)
    assert str(transaction_out.date) == str(
        response.context['outcome_all'][0].date)
    assert str(transaction_out.comment) == str(
        response.context['outcome_all'][0].comment)
    assert transaction_out.enabled == response.context['income_all'][0].enabled


@pytest.mark.django_db
def test_correct_data_for_template_in_one_transaction_reports(client, transaction_in):
    resp = client.get(reverse('transaction_view', args=[
        GeneralTable.objects.last().id]))
    assert resp.context['transaction'].type_of_transaction == transaction_in.type_of_transaction
    assert str(
        resp.context['transaction'].id_section) == str(transaction_in.id_section)
    assert str(
        resp.context['transaction'].id_category) == str(transaction_in.id_category)
    assert str(
        resp.context['transaction'].id_name) == str(transaction_in.id_name)
    assert str(
        resp.context['transaction'].sum_money) == str(transaction_in.sum_money)
    assert str(
        resp.context['transaction'].currency) == str(transaction_in.currency)
    assert str(
        resp.context['transaction'].date) == str(transaction_in.date)
    assert str(
        resp.context['transaction'].comment) == str(transaction_in.comment)
    assert resp.context['transaction'].enabled == transaction_in.enabled


@pytest.mark.django_db
def test_correct_data_for_template_in_transaction_update_reports(client, transaction_in):
    resp = client.get(reverse('transaction_update', args=[
        GeneralTable.objects.last().id]))
    assert resp.context['transaction_form'].type_of_transaction == transaction_in.type_of_transaction
    assert str(resp.context['transaction_form'].id_section) == str(
        transaction_in.id_section)
    assert str(resp.context['transaction_form'].id_category) == str(
        transaction_in.id_category)
    assert str(resp.context['transaction_form'].id_name) == str(
        transaction_in.id_name)
    assert str(resp.context['transaction_form'].sum_money) == str(
        transaction_in.sum_money)
    assert str(resp.context['transaction_form'].currency) == str(
        transaction_in.currency)
    assert str(resp.context['transaction_form'].date) == str(
        transaction_in.date)
    assert str(resp.context['transaction_form'].comment) == str(
        transaction_in.comment)
    assert resp.context['transaction_form'].enabled == transaction_in.enabled


@pytest.mark.django_db
def test_correct_data_for_template_in_transaction_delete_reports(client, transaction_in):
    resp = client.get(reverse('transaction_delete', args=[
        GeneralTable.objects.last().id]))
    assert resp.context['transaction_d_form'].type_of_transaction == transaction_in.type_of_transaction
    assert str(resp.context['transaction_d_form'].id_section) == str(
        transaction_in.id_section)
    assert str(resp.context['transaction_d_form'].id_category) == str(
        transaction_in.id_category)
    assert str(resp.context['transaction_d_form'].id_name) == str(
        transaction_in.id_name)
    assert str(resp.context['transaction_d_form'].sum_money) == str(
        transaction_in.sum_money)
    assert str(resp.context['transaction_d_form'].currency) == str(
        transaction_in.currency)
    assert str(resp.context['transaction_d_form'].date) == str(
        transaction_in.date)
    assert str(resp.context['transaction_d_form'].comment) == str(
        transaction_in.comment)
    assert resp.context['transaction_d_form'].enabled == transaction_in.enabled
