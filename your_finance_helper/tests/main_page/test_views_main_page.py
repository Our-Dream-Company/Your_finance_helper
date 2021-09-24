import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertFormError, assertRaisesMessage
from main_page.models import Section, Category, NameOperation, GeneralTable
from main_page.forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameForm
import datetime
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
def test_published_post_add_new_category(client, create_new_section_in):
    response_category = client.post(reverse('add_new_category'), {
                                    'category': "Банки", 'to_section': create_new_section_in.id})
    assertRedirects(response_category, reverse('add_new_category'))


@pytest.mark.django_db
def test_published_post_add_new_name(client, create_new_category_in):
    response_name = client.post(reverse('add_new_name'), {
                                'name': 'Депозит', 'to_category': create_new_category_in.id})
    assertRedirects(response_name, reverse('add_new_name'))


@pytest.mark.django_db
def test_view_correct_data_in_index_view(client, create_new_transaction_in, create_new_transaction_out):
    response = client.get(reverse('main_page'))
    assert 'Инвестиции' in response.context['in_dict_section']
    assert 'id_section__id' in response.context['in_dict_section']['Инвестиции']
    assert 'Банки' in response.context['in_dict_category']
    assert 'id_category__id' in response.context['in_dict_category']['Банки']
    assert 'id_category__to_section' in response.context['in_dict_category']['Банки']
    assert 'Депозит' in response.context['in_dict_name']
    assert 'id_name__to_category' in response.context['in_dict_name']['Депозит']
    assert 'sum' in response.context['in_dict_name']['Депозит']
    assert response.context['in_sum_all'] == Decimal('80000.00')
    assert 'Мои расходы' in response.context['out_dict_section']
    assert 'id_section__id' in response.context['out_dict_section']['Мои расходы']
    assert 'Мелкие расходы' in response.context['out_dict_category']
    assert 'id_category__id' in response.context['out_dict_category']['Мелкие расходы']
    assert 'id_category__to_section' in response.context['out_dict_category']['Мелкие расходы']
    assert 'Магазин' in response.context['out_dict_name']
    assert 'id_name__to_category' in response.context['out_dict_name']['Магазин']
    assert 'sum' in response.context['out_dict_name']['Магазин']
    assert response.context['out_sum_all'] == Decimal('-5000.00')
    assert response.context['in_dict_section']['Инвестиции']['id_section__id'] == response.context['in_dict_category']['Банки']['id_category__to_section']
    assert response.context['in_dict_category']['Банки']['id_category__id'] == response.context['in_dict_name']['Депозит']['id_name__to_category']
    assert response.context['out_dict_section']['Мои расходы']['id_section__id'] == response.context[
        'out_dict_category']['Мелкие расходы']['id_category__to_section']
    assert response.context['out_dict_category']['Мелкие расходы'][
        'id_category__id'] == response.context['out_dict_name']['Магазин']['id_name__to_category']


@pytest.mark.django_db
def test_published_post_add_income_transaction(published_post_add_income_transaction):
    query = GeneralTable.objects.last()
    assert Section.objects.last().section == 'Работа'
    assert Category.objects.last().category == "Подработка"
    assert NameOperation.objects.last().name == 'Клуб'
    assert query.type_of_transaction == "IN"
    assert query.sum_money == Decimal('50000.00')
    assert query.currency == 'BYN'
    assert query.date == datetime.date(2021, 6, 1)
    assert query.comment == 'ква'
    assert query.enabled == False
    assert len(GeneralTable.objects.all()) == 1
    assertRedirects(published_post_add_income_transaction,
                    '/', status_code=302)


@pytest.mark.django_db
def test_published_post_add_outcome_transaction(published_post_add_outcome_transaction):
    query = GeneralTable.objects.last()
    assert Section.objects.last().section == 'Мои расходы'
    assert Category.objects.last().category == "Аптека"
    assert NameOperation.objects.last().name == 'Антибиотики'
    assert query.type_of_transaction == "OUT"
    assert query.sum_money == Decimal('-500.00')
    assert query.currency == 'BYN'
    assert query.date == datetime.date(2021, 6, 3)
    assert query.comment == 'кря'
    assert query.enabled == False
    assert len(GeneralTable.objects.all()) == 1
    assertRedirects(published_post_add_outcome_transaction,
                    '/', status_code=302)


@pytest.mark.django_db
def test_post_without_data_in_add_new_section(post_without_data_in_add_new_section):
    assertFormError(post_without_data_in_add_new_section,
                    'form', 'section', 'Обязательное поле.')


@pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_section(post_with_invalid_key_in_add_new_section):
    with assertRaisesMessage(Section.DoesNotExist, 'Section matching query does not exist.'):
        Section.objects.get(section='Здоровье')


@pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_section():
    with assertRaisesMessage(Section.DoesNotExist, 'Section matching query does not exist.'):
        Section.objects.get(id=15)


@pytest.mark.django_db
def test_post_with_section_not_transferred_in_add_new_section(client):
    response = client.post(reverse('add_new_section'), {})
    assertFormError(response, 'form', '', None)


@pytest.mark.django_db
def test_post_without_data_in_add_new_category(post_without_data_in_add_new_category):
    assertFormError(post_without_data_in_add_new_category,
                    'form', 'category', 'Обязательное поле.')


@pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_category(post_with_invalid_key_in_add_new_category):
    with assertRaisesMessage(Category.DoesNotExist, 'Category matching query does not exist.'):
        Category.objects.get(category='Банки')


@pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_category():
    with assertRaisesMessage(Category.DoesNotExist, 'Category matching query does not exist.'):
        Category.objects.get(id=15)


@pytest.mark.django_db
def test_post_with_section_not_transferred_in_add_new_category(client):
    response = client.post(reverse('add_new_category'), {})
    assertFormError(response, 'form', '', None)


@pytest.mark.django_db
def test_post_without_data_in_add_new_name(post_without_data_in_add_new_name):
    assertFormError(post_without_data_in_add_new_name,
                    'form', 'name', 'Обязательное поле.')


@pytest.mark.django_db
def test_post_with_invalid_key_in_add_new_name(client, post_without_data_in_add_new_name):
    with assertRaisesMessage(NameOperation.DoesNotExist, 'NameOperation matching query does not exist.'):
        NameOperation.objects.get(name='Депозит')


@pytest.mark.django_db
def test_post_with_nonexistent_section_in_add_new_name():
    with assertRaisesMessage(NameOperation.DoesNotExist, 'NameOperation matching query does not exist.'):
        NameOperation.objects.get(id=15)


def test_post_with_section_not_transferred_in_add_new_name(client):
    response = client.post(reverse('add_new_section'), {})
    assertFormError(response, 'form', '', None)
