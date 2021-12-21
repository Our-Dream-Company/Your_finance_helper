from inspect import ArgSpec
from django.http import response
import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertFormError, assertRaisesMessage
from main_page.models import Section, Category, NameOperation, GeneralTable
from main_page.forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameOperationForm
from reports.forms import DateWidgetForm
from decimal import Decimal


@pytest.mark.parametrize('url, template', [
    ('main_page', 'main_page/index.html'),
    ('add_income', 'main_page/add_income.html'),
    ('add_outcome', 'main_page/add_outcome.html'),
    ('add_new_section', 'main_page/add_new_section.html'),
    ('add_new_category', 'main_page/add_new_category.html'),
    ('add_new_name_operation', 'main_page/add_new_name_operation.html')
])
@pytest.mark.django_db
def test_view_uses_correct_template_main_page(authenticated_user, url, template):
    resp = authenticated_user.get(reverse(url))
    assert resp.status_code == 200
    assertTemplateUsed(resp, template)


@pytest.mark.parametrize('url_form, form', [
    ('add_income', AddIncomeForm),
    ('add_outcome', AddOutcomeForm),
    ('add_new_section', AddNewSectionForm),
    ('add_new_category', AddNewCategoryForm),
    ('add_new_name_operation', AddNewNameOperationForm),
    ('main_page', DateWidgetForm)
])
@pytest.mark.django_db
def test_correct_form_main_page(authenticated_user, url_form, form):
    response = authenticated_user.get(reverse(url_form))
    assert isinstance(response.context["form"], form)


@pytest.mark.parametrize('url', [
    ('main_page'),
    ('add_income'),
    ('add_outcome'),
    ('add_new_section'),
    ('add_new_category'),
    ('add_new_name_operation')
])
@pytest.mark.django_db
def test_is_authenticated_main_page(client, url):
    response = client.get(reverse(url))
    assertRedirects(
        response, f"{reverse('login')}?next={reverse(url)}")


@pytest.mark.django_db
def test_published_post_add_new_section(authenticated_user):
    response = authenticated_user.post(reverse('add_new_section'),
                                       {'section': "Инвестиции"})
    assertRedirects(response, reverse('add_new_section'))


@pytest.mark.django_db
def test_published_post_add_new_category(authenticated_user, create_new_section):
    response_category = authenticated_user.post(reverse('add_new_category'), {
        'category': "Банки", 'to_section': create_new_section.id})
    assertRedirects(response_category, reverse('add_new_category'))


@pytest.mark.django_db
def test_published_post_add_new_name_operation(authenticated_user, create_new_category):
    response_name = authenticated_user.post(reverse('add_new_name_operation'), {
        'name_operation': 'Депозит', 'to_category': create_new_category.id})
    assertRedirects(response_name, reverse('add_new_name_operation'))


@pytest.mark.django_db
def test_view_correct_data_in_index_view(transaction_in, transaction_out, authenticated_user):
    response = authenticated_user.get(reverse('main_page'))
    assert str(
        transaction_in.id_section) in response.context['in_dict_section']
    assert int(transaction_in.id_section_id) == response.context['in_dict_section'][str(
        transaction_in.id_section)]['id_section__id']
    assert str(
        transaction_in.id_category) in response.context['in_dict_category']
    assert int(transaction_in.id_category_id) == response.context['in_dict_category'][str(
        transaction_in.id_category)]['id_category__id']
    assert 'id_category__to_section' in response.context['in_dict_category'][str(
        transaction_in.id_category)]
    assert str(
        transaction_in.id_name) in response.context['in_dict_name']
    assert 'id_name__to_category' in response.context['in_dict_name'][str(
        transaction_in.id_name)]
    assert 'sum' in response.context['in_dict_name'][str(
        transaction_in.id_name)]
    assert response.context['in_sum_all'] == Decimal(transaction_in.sum_money)
    assert str(
        transaction_out.id_section) in response.context['out_dict_section']
    assert 'id_section__id' in response.context['out_dict_section'][str(
        transaction_out.id_section)]
    assert str(
        transaction_out.id_category) in response.context['out_dict_category']
    assert 'id_category__id' in response.context['out_dict_category'][str(
        transaction_out.id_category)]
    assert 'id_category__to_section' in response.context['out_dict_category'][str(
        transaction_out.id_category)]
    assert str(
        transaction_out.id_name) in response.context['out_dict_name']
    assert 'id_name__to_category' in response.context['out_dict_name'][str(
        transaction_out.id_name)]
    assert 'sum' in response.context['out_dict_name'][str(
        transaction_out.id_name)]
    assert response.context['out_sum_all'] == Decimal(
        transaction_out.sum_money)
    assert response.context['in_dict_section'][str(transaction_in.id_section)]['id_section__id'] == response.context['in_dict_category'][str(
        transaction_in.id_category)]['id_category__to_section']
    assert response.context['in_dict_category'][str(transaction_in.id_category)]['id_category__id'] == response.context['in_dict_name'][str(
        transaction_in.id_name)]['id_name__to_category']
    assert response.context['out_dict_section'][str(transaction_out.id_section)]['id_section__id'] == response.context[
        'out_dict_category'][str(transaction_out.id_category)]['id_category__to_section']
    assert response.context['out_dict_category'][str(transaction_out.id_category)][
        'id_category__id'] == response.context['out_dict_name'][str(transaction_out.id_name)]['id_name__to_category']


@pytest.mark.django_db
def test_published_post_add_income_transaction(transaction_in, authenticated_user):
    url = reverse('add_income')
    data = {
        'id_section': transaction_in.id_section,
        'id_category': transaction_in.id_category,
        'id_name': transaction_in.id_name,
        'sum_money': transaction_in.sum_money,
        'currency': transaction_in.currency,
        'date': transaction_in.date,
        'comment': transaction_in.comment
    }
    response = authenticated_user.post(url, data)
    resp_data = response.context['form']
    assert str(transaction_in.id_section) == resp_data['id_section'].data
    assert str(transaction_in.id_category) == resp_data['id_category'].data
    assert str(transaction_in.id_name) == resp_data['id_name'].data
    assert transaction_in.type_of_transaction == 'IN'
    assert Decimal(transaction_in.sum_money) == Decimal(
        resp_data['sum_money'].data)
    assert str(transaction_in.currency) == resp_data['currency'].data
    assert str(transaction_in.date) == resp_data['date'].data
    assert str(transaction_in.comment) == resp_data['comment'].data
    assert transaction_in.enabled == False
    assert GeneralTable.objects.count() == 1


@pytest.mark.django_db
def test_published_post_add_outcome_transaction(authenticated_user, transaction_out):
    url = reverse('add_outcome')
    data = {
        'id_section': transaction_out.id_section,
        'id_category': transaction_out.id_category,
        'id_name': transaction_out.id_name,
        'sum_money': transaction_out.sum_money,
        'currency': transaction_out.currency,
        'date': transaction_out.date,
        'comment': transaction_out.comment
    }
    response = authenticated_user.post(url, data)
    resp_data = response.context['form']
    assert str(transaction_out.id_section) == resp_data['id_section'].data
    assert str(transaction_out.id_category) == resp_data['id_category'].data
    assert str(transaction_out.id_name) == resp_data['id_name'].data
    assert transaction_out.type_of_transaction == 'OUT'
    assert Decimal(transaction_out.sum_money) == Decimal(
        resp_data['sum_money'].data)
    assert str(transaction_out.currency) == resp_data['currency'].data
    assert str(transaction_out.date) == resp_data['date'].data
    assert str(transaction_out.comment) == resp_data['comment'].data
    assert transaction_out.enabled == False
    assert GeneralTable.objects.count() == 1


@pytest.mark.django_db
def test_post_without_data_in_add_new_section(authenticated_user):
    response = authenticated_user.post(
        reverse('add_new_section'), {'section': ''})
    assertFormError(response, 'form', 'section',
                    'Это поле обязательно для заполнения.')


@pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_section(authenticated_user):
    authenticated_user.post(reverse('add_new_section'),
                            {'invalid_key': 'Здоровье'})
    with assertRaisesMessage(Section.DoesNotExist, 'Section matching query does not exist.'):
        Section.objects.get(section='Здоровье')


@pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_section(authenticated_user):
    authenticated_user.get(reverse('add_new_section'))
    with assertRaisesMessage(Section.DoesNotExist, 'Section matching query does not exist.'):
        Section.objects.get(id=15)


@pytest.mark.django_db
def test_post_with_section_not_transferred_in_add_new_section(authenticated_user):
    authenticated_user.get(reverse('add_new_section'))
    response = authenticated_user.post(reverse('add_new_section'), {})
    assertFormError(response, 'form', '', None)


@pytest.mark.django_db
def test_post_without_data_in_add_new_category(authenticated_user, create_new_section):
    response = authenticated_user.post(reverse('add_new_category'), {
        'category': "", 'to_section': create_new_section})
    assertFormError(response, 'form', 'category',
                    'Это поле обязательно для заполнения.')


@pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_category(authenticated_user, create_new_section):
    authenticated_user.post(reverse('add_new_category'), {
        'invalid_key': "Банки", 'to_section': create_new_section})
    with assertRaisesMessage(Category.DoesNotExist, 'Category matching query does not exist.'):
        Category.objects.get(category='Банки')


@pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_category(authenticated_user):
    authenticated_user.get(reverse('add_new_category'))
    with assertRaisesMessage(Category.DoesNotExist, 'Category matching query does not exist.'):
        Category.objects.get(id=15)


@pytest.mark.django_db
def test_post_with_section_not_transferred_in_add_new_category(authenticated_user):
    response = authenticated_user.post(reverse('add_new_category'), {})
    assertFormError(response, 'form', '', None)


@pytest.mark.django_db
def test_post_without_data_in_add_new_name_operation(authenticated_user, create_new_category):
    response = authenticated_user.post(reverse('add_new_name_operation'), {
        'name_operation': '', 'to_category': create_new_category})
    assertFormError(response, 'form', 'name_operation',
                    'Это поле обязательно для заполнения.')


@pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_name_operation(authenticated_user, create_new_category):
    authenticated_user.post(reverse('add_new_name_operation'), {
        'invalid_key': 'Депозит', 'to_category': create_new_category})
    with assertRaisesMessage(NameOperation.DoesNotExist, 'NameOperation matching query does not exist.'):
        NameOperation.objects.get(name_operation='Депозит')


@pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_name_operation(authenticated_user):
    authenticated_user.get(reverse('add_new_name_operation'))
    with assertRaisesMessage(NameOperation.DoesNotExist, 'NameOperation matching query does not exist.'):
        NameOperation.objects.get(id=15)
