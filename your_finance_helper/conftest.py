import pytest
from main_page.models import Section, Category, NameOperation, GeneralTable
from decimal import Decimal
from datetime import datetime


@pytest.fixture()
def create_new_section():
    return Section.objects.create(section="Инвестиции")


@pytest.fixture()
def create_new_category(create_new_section):
    return Category.objects.create(category="Банки", to_section=create_new_section)


@pytest.fixture()
def create_new_name_operation(create_new_category):
    return NameOperation.objects.create(name_operation="Депозит", to_category=create_new_category)


@pytest.fixture
def big_table_factory(create_new_category, create_new_name_operation):
    def wrapper(type):
        return GeneralTable.objects.create(
            type_of_transaction=type,
            id_section=create_new_category.to_section,
            id_category=create_new_category,
            id_name=create_new_name_operation,
            sum_money=Decimal('80000.00'),
            currency='BYN',
            date=datetime.now().date(),
            comment='доходики',
            enabled=False)
    return wrapper


@pytest.fixture
def transaction_in(big_table_factory):
    return big_table_factory(type="IN")


@pytest.fixture
def transaction_out(big_table_factory):
    return big_table_factory(type="OUT")
