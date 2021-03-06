import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed
from main_page.models import GeneralTable
from reports.forms import TransactionUpdateForm, TransactionDeleteForm, DateWidgetForm


@pytest.mark.parametrize('url, template', [
    ('reports', 'reports/reports.html'),
    ('detailed_current_financial_results',
     'reports/detailed_current_financial_results.html'),
])
@pytest.mark.django_db
def test_view_uses_correct_template_reports(authenticated_user, url, template):
    resp = authenticated_user.get(reverse(url))
    assert resp.status_code == 200
    assertTemplateUsed(resp, template)


@pytest.mark.django_db
def test_view_uses_correct_template_one_transaction_reports(authenticated_user, transaction_in):
    resp = authenticated_user.get(reverse('transaction_view', args=[
        transaction_in.id]))
    assert resp.status_code, 200
    assertTemplateUsed(
        resp, 'reports/transaction_view.html')


@pytest.mark.django_db
def test_view_uses_correct_template_transaction_update_reports(authenticated_user, transaction_in):
    resp = authenticated_user.get(reverse('transaction_update', args=[
        transaction_in.id]))
    assert resp.status_code == 200
    assertTemplateUsed(
        resp, 'reports/transaction_update.html')


@pytest.mark.django_db
def test_view_uses_correct_template_transaction_delete_reports(authenticated_user, transaction_in):
    resp = authenticated_user.get(reverse('transaction_delete', args=[
        transaction_in.id]))
    assert resp.status_code, 200
    assertTemplateUsed(
        resp, 'reports/transaction_delete.html')


@pytest.mark.django_db
def test_correct_form_in_transaction_update_reports(authenticated_user, transaction_in):
    response = authenticated_user.get(reverse('transaction_update', args=[
        transaction_in.id]))
    assert isinstance(
        response.context['form'], TransactionUpdateForm)


@pytest.mark.django_db
def test_correct_form_in_transaction_transaction_delete(authenticated_user, transaction_in):
    response = authenticated_user.get(reverse('transaction_delete', args=[
        transaction_in.id]))
    assert isinstance(
        response.context['form'], TransactionDeleteForm)


@pytest.mark.django_db
def test_correct_form_in_transaction_detailed_current_financial_results(authenticated_user):
    response = authenticated_user.get(
        reverse('detailed_current_financial_results'))
    assert isinstance(
        response.context['form'], DateWidgetForm)


@pytest.mark.parametrize('url', [
    ('reports'),
    ('detailed_current_financial_results'),
])
@pytest.mark.django_db
def test_is_authenticated_reports(client, url):
    response = client.get(reverse(url))
    assertRedirects(
        response, f"{reverse('login')}?next={reverse(url)}")


@pytest.mark.django_db
def test_correct_data_for_template_in_detailed_current_financial_results_reports(authenticated_user, transaction_in, transaction_out):
    response = authenticated_user.get(
        reverse('detailed_current_financial_results'))
    resp_data_in = response.context['income_all'][0]
    resp_data_out = response.context['outcome_all'][0]
    assert str(transaction_in.type_of_transaction) == str(
        resp_data_in.type_of_transaction)
    assert str(transaction_in.id_section) == str(resp_data_in.id_section)
    assert str(transaction_in.id_category) == str(resp_data_in.id_category)
    assert str(transaction_in.id_name) == str(resp_data_in.id_name)
    assert str(transaction_in.sum_money) == str(resp_data_in.sum_money)
    assert str(transaction_in.currency) == str(resp_data_in.currency)
    assert str(transaction_in.date) == str(resp_data_in.date)
    assert str(transaction_in.comment) == str(resp_data_in.comment)
    assert transaction_in.enabled == resp_data_in.enabled
    assert str(transaction_out.type_of_transaction) == str(
        resp_data_out.type_of_transaction)
    assert str(transaction_out.id_section) == str(resp_data_out.id_section)
    assert str(transaction_out.id_category) == str(resp_data_out.id_category)
    assert str(transaction_out.id_name) == str(resp_data_out.id_name)
    assert str(transaction_out.sum_money) == str(resp_data_out.sum_money)
    assert str(transaction_out.currency) == str(resp_data_out.currency)
    assert str(transaction_out.date) == str(resp_data_out.date)
    assert str(transaction_out.comment) == str(resp_data_out.comment)
    assert transaction_out.enabled == resp_data_out.enabled


@pytest.mark.django_db
def test_correct_data_for_template_in_one_transaction_reports(authenticated_user, transaction_in):
    resp = authenticated_user.get(reverse('transaction_view', args=[
        GeneralTable.objects.last().id]))
    resp_data = resp.context['transaction']
    assert resp_data.type_of_transaction == transaction_in.type_of_transaction
    assert str(resp_data.id_section) == str(transaction_in.id_section)
    assert str(resp_data.id_category) == str(transaction_in.id_category)
    assert str(resp_data.id_name) == str(transaction_in.id_name)
    assert str(resp_data.sum_money) == str(transaction_in.sum_money)
    assert str(resp_data.currency) == str(transaction_in.currency)
    assert str(resp_data.date) == str(transaction_in.date)
    assert str(resp_data.comment) == str(transaction_in.comment)
    assert resp_data.enabled == transaction_in.enabled


@pytest.mark.django_db
def test_correct_data_for_template_in_transaction_update_reports(authenticated_user, transaction_in):
    resp = authenticated_user.get(reverse('transaction_update', args=[
        GeneralTable.objects.last().id]))
    resp_data = resp.context['transaction_form']
    assert resp_data.type_of_transaction == transaction_in.type_of_transaction
    assert str(resp_data.id_section) == str(transaction_in.id_section)
    assert str(resp_data.id_category) == str(transaction_in.id_category)
    assert str(resp_data.id_name) == str(transaction_in.id_name)
    assert str(resp_data.sum_money) == str(transaction_in.sum_money)
    assert str(resp_data.currency) == str(transaction_in.currency)
    assert str(resp_data.date) == str(transaction_in.date)
    assert str(resp_data.comment) == str(transaction_in.comment)
    assert resp_data.enabled == transaction_in.enabled


@pytest.mark.django_db
def test_correct_data_for_template_in_transaction_delete_reports(authenticated_user, transaction_in):
    resp = authenticated_user.get(reverse('transaction_delete', args=[
        GeneralTable.objects.last().id]))
    resp_data = resp.context['transaction_d_form']
    assert resp_data .type_of_transaction == transaction_in.type_of_transaction
    assert str(resp_data.id_section) == str(transaction_in.id_section)
    assert str(resp_data.id_category) == str(transaction_in.id_category)
    assert str(resp_data.id_name) == str(transaction_in.id_name)
    assert str(resp_data.sum_money) == str(transaction_in.sum_money)
    assert str(resp_data.currency) == str(transaction_in.currency)
    assert str(resp_data.date) == str(transaction_in.date)
    assert str(resp_data.comment) == str(transaction_in.comment)
    assert resp.context['transaction_d_form'].enabled == transaction_in.enabled
