import pytest
from main_page.models import Section, Category, NameOperation, GeneralTable
from main_page.forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameForm
from decimal import Decimal
from django.urls import reverse


@pytest.fixture()
def create_new_section_in():
    return Section.objects.create(section="Инвестиции")


@pytest.fixture()
def create_new_section_out():
    return Section.objects.create(section="Мои расходы")


@pytest.fixture()
def create_new_category_in(create_new_section_in):
    return Category.objects.create(category="Банки", to_section=create_new_section_in)


@pytest.fixture()
def create_new_category_out(create_new_section_out):
    return Category.objects.create(category="Мелкие расходы", to_section=create_new_section_out)


@pytest.fixture()
def create_new_name_in(create_new_category_in):
    return NameOperation.objects.create(name="Депозит", to_category=create_new_category_in)


@pytest.fixture()
def create_new_name_out(create_new_category_out):
    return NameOperation.objects.create(name="Магазин", to_category=create_new_category_out)


@pytest.fixture()
def create_new_transaction_in(create_new_section_in, create_new_category_in, create_new_name_in):
    return GeneralTable.objects.create(
        type_of_transaction="IN",
        id_section=create_new_section_in,
        id_category=create_new_category_in,
        id_name=create_new_name_in,
        sum_money=Decimal('80000.00'),
        currency='BYN',
        date="2021-06-03",
        comment='доходики',
        enabled=False
    )


@pytest.fixture()
def create_new_transaction_out(create_new_section_out, create_new_category_out, create_new_name_out):
    return GeneralTable.objects.create(
        type_of_transaction="OUT",
        id_section=create_new_section_out,
        id_category=create_new_category_out,
        id_name=create_new_name_out,
        sum_money=Decimal('-5000.00'),
        currency='BYN',
        date="2021-06-01",
        comment='расходики',
        enabled=False
    )


@pytest.fixture()
def published_post_add_income_transaction(client):
    client.post(
        '/add_new_section', {'section': "Работа"})
    client.post(
        '/add_new_category', {'category': "Подработка", 'to_section': Section.objects.last().id})
    client.post(
        '/add_new_name', {'name': 'Клуб', 'to_category': Category.objects.last().id})
    response_general_table_income = client.post(
        '/add_income', {'type_of_transaction': "IN",
                        'id_section': Section.objects.last().id,
                        'id_category': Category.objects.last().id,
                        'id_name': NameOperation.objects.last().id,
                        'sum_money': Decimal('50000.00'),
                        'currency': 'BYN',
                        'date': "2021-06-01",
                        'comment': 'ква',
                        'enabled': False
                        }
    )
    return response_general_table_income


@pytest.fixture()
def published_post_add_outcome_transaction(client):
    client.post(
        '/add_new_section', {'section': "Мои расходы"})
    client.post(
        '/add_new_category', {'category': "Аптека", 'to_section': Section.objects.last().id})
    client.post(
        '/add_new_name', {'name': 'Антибиотики', 'to_category': Category.objects.last().id})
    response_general_table_outcome = client.post(
        '/add_outcome', {'type_of_transaction': "OUT",
                         'id_section': Section.objects.last().id,
                         'id_category': Category.objects.last().id,
                         'id_name': NameOperation.objects.last().id,
                         'sum_money': Decimal('-500.00'),
                         'currency': 'BYN',
                         'date': "2021-06-03",
                         'comment': 'кря',
                         'enabled': False
                         }
    )
    return response_general_table_outcome


@pytest.fixture()
def post_without_data_in_add_new_section(client):
    return client.post(reverse('add_new_section'), {'section': ''})


@pytest.fixture()
def post_with_invalid_key_in_add_new_section(client):
    return client.post(reverse('add_new_section'), {'invalid_key': 'Здоровье'})


@pytest.fixture()
def post_without_data_in_add_new_category(client, create_new_section_in):
    return client.post(reverse('add_new_category'), {'category': "", 'to_section': create_new_section_in})


@pytest.fixture()
def post_with_invalid_key_in_add_new_category(client, create_new_section_in):
    return client.post(reverse('add_new_category'), {
        'invalid_key': "Банки", 'to_section': create_new_section_in})


@pytest.fixture()
def post_without_data_in_add_new_name(client, create_new_category_in):
    return client.post(reverse('add_new_name'), {'name': '', 'to_category': create_new_category_in})


@pytest.fixture()
def post_without_data_in_add_new_name(client, create_new_category_in):
    return client.post(reverse('add_new_name'), {'invalid_key': 'Депозит', 'to_category': create_new_category_in})
