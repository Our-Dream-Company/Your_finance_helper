import datetime
from django.http import response
from django.http import HttpResponsePermanentRedirect
from django.test import TestCase
from decimal import Decimal
from unittest import mock
from django.test.client import Client
from main_page.models import Section, Category, NameOperation, GeneralTable
from django.urls import reverse, resolve
from reports.views import ReportsButtonsView, DetailedCurrentFinancialResultsView, TransactionView, TransactionUpdateView, TransactionDeleteView


class ReportsButtonsViewTest(TestCase):
    def test_view_url_reports(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_reports(self):
        resp = self.client.get(reverse('reports'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_reports(self):
        resp = self.client.get(reverse('reports'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'reports/reports.html')

    def test_main_page_url_resolves_reports_name(self):
        resolver = resolve('/reports/')
        self.assertEqual(resolver.view_name, 'reports')
        self.assertEqual(resolver.url_name, 'reports')

    def test_url_resolves_to_reports_transactions_view(self):
        found = resolve('/reports/')
        self.assertEqual(found.func.view_class, ReportsButtonsView)


class DetailedCurrentFinancialResultsViewTest(TestCase):
    def test_view_url_detailed_current_financial_results_reports(self):
        resp = self.client.get('/reports/detailed_current_financial_results')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_detailed_current_financial_results_reports(self):
        resp = self.client.get(reverse('detailed_current_financial_results'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template__detailed_current_financial_results_reports(self):
        resp = self.client.get(reverse('detailed_current_financial_results'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/detailed_current_financial_results.html')

    def test_main_page_url_resolves_detailed_current_financial_results_reports_name(self):
        resolver = resolve('/reports/detailed_current_financial_results')
        self.assertEqual(resolver.view_name,
                         'detailed_current_financial_results')
        self.assertEqual(resolver.url_name,
                         'detailed_current_financial_results')

    def test_url_resolves_to_reports_transactions_view(self):
        found = resolve('/reports/detailed_current_financial_results')
        self.assertEqual(found.func.view_class,
                         DetailedCurrentFinancialResultsView)


class TransactionViewTest(TestCase):
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

    def test_view_url_one_transaction_reports(self):
        view = self.client.get(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id))
        self.assertEqual(view.status_code, 200)

    def test_view_url_accessible_by_name_one_transaction_reports(self):
        resp = self.client.get(reverse('transaction_view', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_one_transaction_reports(self):
        resp = self.client.get(reverse('transaction_view', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/transaction_view.html')

    def test_main_page_url_resolves_one_transaction_reports_name(self):
        resolver = resolve(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id))
        self.assertEqual(resolver.view_name,
                         'transaction_view')
        self.assertEqual(resolver.url_name,
                         'transaction_view')

    def test_url_resolves_to_reports_transactions_view(self):
        found = resolve(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id))
        self.assertEqual(found.func.view_class, TransactionView)


class TransactionUpdateViewTest(TestCase):
    def setUp(self):
        section = Section.objects.create(section="Мои расходы")
        category = Category.objects.create(
            category="Мелкие расходы", to_section=section)
        name = NameOperation.objects.create(
            name="Магазин", to_category=category)
        general_table = GeneralTable.objects.create(
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

    def test_view_url_transaction_update_reports(self):
        view = self.client.get(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id) + '/update')
        self.assertEqual(view.status_code, 200)

    def test_view_url_accessible_by_name_transaction_update_reports(self):
        resp = self.client.get(reverse('transaction_update', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_transaction_update_reports(self):
        resp = self.client.get(reverse('transaction_update', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/transaction_update.html')

    def test_main_page_url_resolves_transaction_update_reports(self):
        resolver = resolve(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id) + '/update')
        self.assertEqual(resolver.view_name,
                         'transaction_update')
        self.assertEqual(resolver.url_name,
                         'transaction_update')

    def test_url_resolves_to_reports_transactions_view(self):
        found = resolve(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id) + '/update')
        self.assertEqual(found.func.view_class, TransactionUpdateView)


class TransactionDeleteViewTest(TestCase):
    def setUp(self):
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

    def test_view_url_transaction_delete_reports(self):
        view = self.client.get(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id) + '/delete')
        self.assertEqual(view.status_code, 200)

    def test_view_url_accessible_by_name_transaction_delete_reports(self):
        resp = self.client.get(reverse('transaction_delete', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_transaction_delete_reports(self):
        resp = self.client.get(reverse('transaction_delete', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/transaction_delete.html')

    def test_main_page_url_resolves_transaction_delete_reports(self):
        resolver = resolve(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id) + '/delete')
        self.assertEqual(resolver.view_name,
                         'transaction_delete')
        self.assertEqual(resolver.url_name,
                         'transaction_delete')

    def test_url_resolves_to_reports_transactions_view(self):
        found = resolve(
            '/reports/detailed_current_financial_results/' + str(GeneralTable.objects.last().id) + '/delete')
        self.assertEqual(found.func.view_class, TransactionDeleteView)
