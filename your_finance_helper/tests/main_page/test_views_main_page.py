import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertFormError, assertRaisesMessage
from main_page.models import Section, Category, NameOperation, GeneralTable
from main_page.forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameForm
from decimal import Decimal


@pytest.mark.django_db
def test_view_uses_correct_template_main_page(client):
    resp = client.get(reverse('main_page'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'main_page/index.html')


@pytest.mark.django_db
def test_view_uses_correct_template_add_income(client):
    resp = client.get(reverse('add_income'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'main_page/add_income.html')


@pytest.mark.django_db
def test_view_uses_correct_template_add_outcome(client):
    resp = client.get(reverse('add_outcome'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'main_page/add_outcome.html')


@pytest.mark.django_db
def test_view_uses_correct_template_add_new_section(client):
    resp = client.get(reverse('add_new_section'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'main_page/add_new_section.html')


@pytest.mark.django_db
def test_view_uses_correct_template_add_new_category(client):
    resp = client.get(reverse('add_new_category'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'main_page/add_new_category.html')


@pytest.mark.django_db
def test_view_uses_correct_template_add_new_name(client):
    resp = client.get(reverse('add_new_name'))
    assert resp.status_code == 200
    assertTemplateUsed(resp, 'main_page/add_new_name.html')


@pytest.mark.django_db
def test_correct_form_in_add_incomecome_transaction(client):
    response = client.get(reverse('add_income'))
    assert isinstance(response.context["form"], AddIncomeForm)
    assert response.context['form'].instance.type_of_transaction == 'IN'


@pytest.mark.django_db
def test_correct_form_in_add_outcome_transaction(client):
    response = client.get(reverse('add_outcome'))
    assert isinstance(response.context["form"], AddOutcomeForm)
    assert response.context['form'].instance.type_of_transaction == 'OUT'


@pytest.mark.django_db
def test_correct_form_in_add_new_section(client):
    response = client.get(reverse('add_new_section'))
    assert isinstance(response.context["form"], AddNewSectionForm)


@pytest.mark.django_db
def test_correct_form_in_add_new_category(client):
    response = client.get(reverse('add_new_category'))
    assert isinstance(response.context["form"], AddNewCategoryForm)


@pytest.mark.django_db
def test_correct_form_in_add_new_name(client):
    response = client.get(reverse('add_new_name'))
    assert isinstance(response.context["form"], AddNewNameForm)


@pytest.mark.django_db
def test_published_post_add_new_section(client):
    response = client.post(reverse('add_new_section'),
                           {'section': "Инвестиции"})
    assertRedirects(response, reverse('add_new_section'))


@pytest.mark.django_db
def test_published_post_add_new_category(client, create_new_section):
    response_category = client.post(reverse('add_new_category'), {
                                    'category': "Банки", 'to_section': create_new_section.id})
    assertRedirects(response_category, reverse('add_new_category'))


@pytest.mark.django_db
def test_published_post_add_new_name(client, create_new_category):
    response_name = client.post(reverse('add_new_name'), {
                                'name': 'Депозит', 'to_category': create_new_category.id})
    assertRedirects(response_name, reverse('add_new_name'))


@pytest.mark.django_db
def test_view_correct_data_in_index_view(client, transaction_in, transaction_out):
    response = client.get(reverse('main_page'))
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
    print(response.context['out_dict_category']
          [str(transaction_out.id_category)])
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


@ pytest.mark.django_db
def test_published_post_add_income_transaction(client, transaction_in):
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
    response = client.post(url, data)
    assert str(
        transaction_in.id_section) == response.context['form']['id_section'].data
    assert str(
        transaction_in.id_category) == response.context['form']['id_category'].data
    assert str(
        transaction_in.id_name) == response.context['form']['id_name'].data
    assert transaction_in.type_of_transaction == 'IN'
    assert Decimal(transaction_in.sum_money) == Decimal(
        response.context['form']['sum_money'].data)
    assert str(
        transaction_in.currency) == response.context['form']['currency'].data
    assert str(
        transaction_in.date) == response.context['form']['date'].data
    assert str(
        transaction_in.comment) == response.context['form']['comment'].data
    assert transaction_in.enabled == False
    assert GeneralTable.objects.count() == 1


@ pytest.mark.django_db
def test_published_post_add_outcome_transaction(client, transaction_out):
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
    response = client.post(url, data)
    assert str(
        transaction_out.id_section) == response.context['form']['id_section'].data
    assert str(
        transaction_out.id_category) == response.context['form']['id_category'].data
    assert str(
        transaction_out.id_name) == response.context['form']['id_name'].data
    assert transaction_out.type_of_transaction == 'OUT'
    assert Decimal(transaction_out.sum_money) == Decimal(
        response.context['form']['sum_money'].data)
    assert str(
        transaction_out.currency) == response.context['form']['currency'].data
    assert str(
        transaction_out.date) == response.context['form']['date'].data
    assert str(
        transaction_out.comment) == response.context['form']['comment'].data
    assert transaction_out.enabled == False
    assert GeneralTable.objects.count() == 1


@ pytest.mark.django_db
def test_post_without_data_in_add_new_section(client):
    response = client.post(reverse('add_new_section'), {'section': ''})
    assertFormError(response, 'form', 'section', 'Обязательное поле.')


@ pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_section(client):
    client.post(reverse('add_new_section'), {'invalid_key': 'Здоровье'})
    with assertRaisesMessage(Section.DoesNotExist, 'Section matching query does not exist.'):
        Section.objects.get(section='Здоровье')


@ pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_section(client):
    client.get(reverse('add_new_section'))
    with assertRaisesMessage(Section.DoesNotExist, 'Section matching query does not exist.'):
        Section.objects.get(id=15)


@ pytest.mark.django_db
def test_post_with_section_not_transferred_in_add_new_section(client):
    client.get(reverse('add_new_section'))
    response = client.post(reverse('add_new_section'), {})
    assertFormError(response, 'form', '', None)


@ pytest.mark.django_db
def test_post_without_data_in_add_new_category(client, create_new_section):
    response = client.post(reverse('add_new_category'), {
        'category': "", 'to_section': create_new_section})
    assertFormError(response, 'form', 'category', 'Обязательное поле.')


@ pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_category(client, create_new_section):
    client.post(reverse('add_new_category'), {
                'invalid_key': "Банки", 'to_section': create_new_section})
    with assertRaisesMessage(Category.DoesNotExist, 'Category matching query does not exist.'):
        Category.objects.get(category='Банки')


@ pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_category(client):
    client.get(reverse('add_new_category'))
    with assertRaisesMessage(Category.DoesNotExist, 'Category matching query does not exist.'):
        Category.objects.get(id=15)


@ pytest.mark.django_db
def test_post_with_section_not_transferred_in_add_new_category(client):
    response = client.post(reverse('add_new_category'), {})
    assertFormError(response, 'form', '', None)


@ pytest.mark.django_db
def test_post_without_data_in_add_new_name(client, create_new_category):
    response = client.post(reverse('add_new_name'), {
        'name': '', 'to_category': create_new_category})
    assertFormError(response, 'form', 'name', 'Обязательное поле.')


@ pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_name(client, create_new_category):
    client.post(reverse('add_new_name'), {
                'invalid_key': 'Депозит', 'to_category': create_new_category})
    with assertRaisesMessage(NameOperation.DoesNotExist, 'NameOperation matching query does not exist.'):
        NameOperation.objects.get(name='Депозит')


@ pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_name(client):
    client.get(reverse('add_new_name'))
    with assertRaisesMessage(NameOperation.DoesNotExist, 'NameOperation matching query does not exist.'):
        NameOperation.objects.get(id=15)


def test_post_with_section_not_transferred_in_add_new_name(client):
    response = client.post(reverse('add_new_section'), {})
    assertFormError(response, 'form', '', None)
