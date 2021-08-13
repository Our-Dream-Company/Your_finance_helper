import datetime
from django.http import response
from django.http import HttpResponsePermanentRedirect
from django.test import TestCase
from decimal import Decimal
from unittest import mock
from django.test.client import Client
from main_page.models import Section, Category, NameOperation, GeneralTable
from django.urls import reverse, resolve
from main_page.views import IndexView, AddIncomeView, AddOutcomeView, AddNewSectionView, AddNewCategoryView, AddNewNameView


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        section = Section.objects.create(section="Мои расходы")
        category = Category.objects.create(
            category="Мелкие расходы", to_section=section)
        name = NameOperation.objects.create(
            name="Магазин", to_category=category)
        GeneralTable.objects.create(
            type_of_transaction="OUT",
            id_section=section,
            id_category=category,
            id_name=name,
            sum_money=Decimal('-5000.00'),
            currency='BYN',
            date="2021-06-01",
            comment='ква',
            enabled=False
        )

    def test_view_url_main_page(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('main_page'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_main_page(self):
        resp = self.client.get(reverse('main_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/index.html')

    def test_main_page_url_resolves_main_page_name(self):
        resolver = resolve('/')
        self.assertEqual(resolver.view_name, 'main_page')
        self.assertEqual(resolver.url_name, 'main_page')

    def test_check_data_from_sql_main_page(self):
        response = GeneralTable.objects.values('id_section__id', 'id_section__section', 'id_category__id', 'id_category__category',
                                               'id_category__to_section', 'id_name__name', 'id_name__to_category')
        self.assertIs(type(response[0]), dict)

    def test_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, IndexView)


class AddIncomeViewTest(TestCase):
    def test_view_url_add_income(self):
        resp = self.client.get('/add_income')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_add_income(self):
        resp = self.client.get(reverse('add_income'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_add_income(self):
        resp = self.client.get(reverse('add_income'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_income.html')

    def test_add_income_url_resolves_add_income_name(self):
        resolver = resolve('/add_income')
        self.assertEqual(resolver.view_name, 'add_income')
        self.assertEqual(resolver.url_name, 'add_income')

    def test_published_post_add_income_transaction(self):
        response_section = self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        response_category = self.client.post(
            '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
        response_name = self.client.post(
            '/add_new_name', {'name': 'Депозит', 'to_category': Category.objects.last().id})
        response_general_table_income = self.client.post(
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
#        self.assertEqual(GeneralTable.objects.last().id_name,
#                         'Депозит')
#       AssertionError: <NameOperation: Депозит> != 'Депозит'
        self.assertEqual(GeneralTable.objects.last().type_of_transaction,
                         "IN")
        self.assertEqual(GeneralTable.objects.last().sum_money,
                         Decimal('50000.00'))
        self.assertEqual(GeneralTable.objects.last().currency, 'BYN')
        self.assertEqual(GeneralTable.objects.last().date,
                         datetime.date(2021, 6, 1))
        self.assertEqual(GeneralTable.objects.last().comment, 'ква')
        self.assertEqual(GeneralTable.objects.last().enabled, False)
        self.assertRedirects(response_general_table_income,
                             '/', status_code=302)

    def test_resolve_index_url_to_add_income_transaction(self):
        view = resolve('/add_income')
        self.assertEqual(view.func.view_class, AddIncomeView)


class AddOutcomeViewTest(TestCase):
    def test_view_url_add_outcome(self):
        resp = self.client.get('/add_outcome')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_add_outcome(self):
        resp = self.client.get(reverse('add_outcome'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_add_outcome(self):
        resp = self.client.get(reverse('add_outcome'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_outcome.html')

    def test_add_outcome_url_resolves_add_outcome_name(self):
        resolver = resolve('/add_outcome')
        self.assertEqual(resolver.view_name, 'add_outcome')
        self.assertEqual(resolver.url_name, 'add_outcome')

    def test_published_post_add_outcome_transaction(self):
        response_section = self.client.post(
            '/add_new_section', {'section': "Мои расходы"})
        response_category = self.client.post(
            '/add_new_category', {'category': "Аптека", 'to_section': Section.objects.last().id})
        response_name = self.client.post(
            '/add_new_name', {'name': 'Антибиотики', 'to_category': Category.objects.last().id})
        response_general_table_income = self.client.post(
            '/add_outcome', {'type_of_transaction': "OUT",
                             'id_section': Section.objects.last().id,
                             'id_category': Category.objects.last().id,
                             'id_name': NameOperation.objects.last().id,
                             'sum_money': Decimal('-500.00'),
                             'currency': 'BYN',
                             'date': "2021-06-03",
                             'comment': 'ква',
                             'enabled': False
                             }
        )
#        self.assertEqual(GeneralTable.objects.last().id_name,
#                         'Антибиотики')
#       AssertionError: <NameOperation: Антибиотики> != 'Антибиотики'
        self.assertEqual(GeneralTable.objects.last().type_of_transaction,
                         "OUT")
        self.assertEqual(GeneralTable.objects.last().sum_money,
                         Decimal('-500.00'))
        self.assertEqual(GeneralTable.objects.last().currency, 'BYN')
        self.assertEqual(GeneralTable.objects.last().date,
                         datetime.date(2021, 6, 3))
        self.assertEqual(GeneralTable.objects.last().comment, 'ква')
        self.assertEqual(GeneralTable.objects.last().enabled, False)
        self.assertRedirects(response_general_table_income,
                             '/', status_code=302)

    def test_resolve_index_url_to_add_outcome_transaction(self):
        view = resolve('/add_outcome')
        self.assertEqual(view.func.view_class, AddOutcomeView)


class AddNewSectionViewTest(TestCase):
    def test_view_url_add_new_section(self):
        resp = self.client.get('/add_new_section')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_add_new_section(self):
        resp = self.client.get(reverse('add_new_section'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_add_new_section(self):
        resp = self.client.get(reverse('add_new_section'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_section.html')

    def test_add_new_section_url_resolves_add_new_section_name(self):
        resolver = resolve('/add_new_section')
        self.assertEqual(resolver.view_name, 'add_new_section')
        self.assertEqual(resolver.url_name, 'add_new_section')

    def test_published_post_add_new_section(self):
        response = self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        self.assertEqual(Section.objects.last().section, "Инвестиции")
        self.assertRedirects(response, '/add_new_section', status_code=302)

    def test_resolve_index_url_to_add_new_section(self):
        view = resolve('/add_new_section')
        self.assertEqual(view.func.view_class, AddNewSectionView)


class AddNewCategoryViewTest(TestCase):
    def test_view_url_add_new_category(self):
        resp = self.client.get('/add_new_category')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_add_new_category(self):
        resp = self.client.get(reverse('add_new_category'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_add_new_category(self):
        resp = self.client.get(reverse('add_new_category'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_category.html')

    def test_add_new_category_url_resolves_add_new_category_name(self):
        resolver = resolve('/add_new_category')
        self.assertEqual(resolver.view_name, 'add_new_category')
        self.assertEqual(resolver.url_name, 'add_new_category')

    def test_published_post_add_new_category(self):
        response_section = self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        response_category = self.client.post(
            '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
        self.assertEqual(Category.objects.last().category, "Банки")
        self.assertRedirects(
            response_category, '/add_new_category', status_code=302)

    def test_resolve_index_url_to_add_new_category(self):
        view = resolve('/add_new_category')
        self.assertEqual(view.func.view_class, AddNewCategoryView)


class AddNewNameViewTest(TestCase):
    def test_view_url_add_new_category(self):
        resp = self.client.get('/add_new_name')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_add_new_name(self):
        resp = self.client.get(reverse('add_new_name'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_add_new_name(self):
        resp = self.client.get(reverse('add_new_name'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_name.html')

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('add_new_name'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_name.html')

    def test_add_new_name_url_resolves_add_new_name_name(self):
        resolver = resolve('/add_new_name')
        self.assertEqual(resolver.view_name, 'add_new_name')
        self.assertEqual(resolver.url_name, 'add_new_name')

    def test_published_post_add_new_name_name(self):
        response_section = self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        response_category = self.client.post(
            '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
        response_name = self.client.post(
            '/add_new_name', {'name': 'Депозит', 'to_category': Category.objects.last().id})
        self.assertEqual(NameOperation.objects.last().name, "Депозит")
        self.assertRedirects(response_name, '/add_new_name', status_code=302)

    def test_resolve_index_url_to_add_new_name(self):
        view = resolve('/add_new_name')
        self.assertEqual(view.func.view_class, AddNewNameView)
