import pytest
from main_page.models import Section, Category, NameOperation, GeneralTable
from decimal import Decimal


@pytest.fixture()
def create_new_section():
    return Section.objects.create(section="Инвестиции")


@pytest.fixture()
def create_new_category(create_new_section):
    return Category.objects.create(category="Банки", to_section=create_new_section)


@pytest.fixture()
def create_new_name(create_new_category):
    return NameOperation.objects.create(name="Депозит", to_category=create_new_category)


@pytest.fixture
def big_table_factory(create_new_category, create_new_name):
    def wrapper(type):
        return GeneralTable.objects.create(
            type_of_transaction=type,
            id_section=create_new_category.to_section,
            id_category=create_new_category,
            id_name=create_new_name,
            sum_money=Decimal('80000.00'),
            currency='BYN',
            date="2021-06-03",
            comment='доходики',
            enabled=False)
    return wrapper


@pytest.fixture
def transaction_in(big_table_factory):
    return big_table_factory(type="IN")


@pytest.fixture
def transaction_out(big_table_factory):
    return big_table_factory(type="OUT")


@pytest.fixture()
def create_new_transaction_in(create_new_category_in, create_new_name_in):
    return GeneralTable.objects.create(
        type_of_transaction="IN",
        id_section=create_new_category_in.to_section,
        id_category=create_new_category_in,
        id_name=create_new_name_in,
        sum_money=Decimal('80000.00'),
        currency='BYN',
        date="2021-06-03",
        comment='доходики',
        enabled=False
    )


@pytest.fixture()
def create_new_transaction_out(create_new_category_out, create_new_name_out):
    return GeneralTable.objects.create(
        type_of_transaction="OUT",
        id_section=create_new_category_out.to_section,
        id_category=create_new_category_out,
        id_name=create_new_name_out,
        sum_money=Decimal('-5000.00'),
        currency='BYN',
        date="2021-06-01",
        comment='расходики',
        enabled=False
    )
