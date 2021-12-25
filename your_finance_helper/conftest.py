from os import system
import pytest
from main_page.models import Section, Category, NameOperation, GeneralTable
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from captcha.conf import settings as captcha_settings


@pytest.fixture()
def captcha_test_mode():
    captcha_settings.CAPTCHA_TEST_MODE = True
    yield
    captcha_settings.CAPTCHA_TEST_MODE = False


@pytest.fixture()
def create_user():
    return User.objects.create_user(
        'john', 'lennon@thebeatles.com', 'Hack1234')


@pytest.fixture
def authenticated_user(client, create_user):
    client.force_login(create_user)
    return client


@pytest.fixture()
def create_new_section(create_user):
    return Section.objects.create(section="Инвестиции", id_user_from_section=create_user)


@pytest.fixture()
def create_new_category(create_new_section, create_user):
    return Category.objects.create(category="Банки", to_section=create_new_section, id_user_from_category=create_user)


@pytest.fixture()
def create_new_name_operation(create_new_category, create_user):
    return NameOperation.objects.create(name_operation="Депозит", to_category=create_new_category, id_user_from_name_operation=create_user)


@pytest.fixture
def big_table_factory(create_new_category, create_new_name_operation, create_user):
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
            enabled=False,
            id_user=create_user
        )
    return wrapper


@pytest.fixture
def transaction_in(big_table_factory):
    return big_table_factory(type="IN")


@pytest.fixture
def transaction_out(big_table_factory):
    return big_table_factory(type="OUT")
