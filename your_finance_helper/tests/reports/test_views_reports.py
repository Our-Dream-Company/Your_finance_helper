from django.test import TestCase
from decimal import Decimal
from main_page.models import Section, Category, NameOperation, GeneralTable
from django.urls import reverse
from reports.forms import TransactionUpdateForm, TransactionDeleteForm


class TestReportsButtonsView(TestCase):
    def test_view_uses_correct_template_reports(self):
        resp = self.client.get(reverse('reports'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'reports/reports.html')


class TestDetailedCurrentFinancialResultsView(TestCase):
    def test_view_uses_correct_template_detailed_current_financial_results_reports(self):
        resp = self.client.get(reverse('detailed_current_financial_results'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/detailed_current_financial_results.html')

    def test_correct_data_for_template_in_detailed_current_financial_results_reports(self):
        self.client.post(
            reverse('add_new_section'), {'section': "Инвестиции"})
        self.client.post(
            reverse('add_new_category'), {'category': "Банки", 'to_section': Section.objects.last().id})
        self.client.post(
            reverse('add_new_name'), {'name': 'Депозит', 'to_category': Category.objects.last().id})
        self.client.post(
            reverse('add_income'), {'type_of_transaction': "IN",
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
        self.client.post(
            reverse('add_new_section'), {'section': "Мои расходы"})
        self.client.post(
            reverse('add_new_category'), {'category': "Аптека", 'to_section': Section.objects.last().id})
        self.client.post(
            reverse('add_new_name'), {'name': 'Антибиотики', 'to_category': Category.objects.last().id})
        self.client.post(
            reverse('add_outcome'), {'type_of_transaction': "OUT",
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
        response = self.client.get(
            reverse('detailed_current_financial_results'))
        self.assertEqual(
            str(response.context['income_all'][0].type_of_transaction), 'IN')
        self.assertEqual(
            str(response.context['income_all'][0].id_section), 'Инвестиции')
        self.assertEqual(
            str(response.context['income_all'][0].id_category), 'Банки')
        self.assertEqual(
            str(response.context['income_all'][0].id_name), 'Депозит')
        self.assertEqual(
            str(response.context['income_all'][0].sum_money), '50000.00')
        self.assertEqual(
            str(response.context['income_all'][0].currency), 'BYN')
        self.assertEqual(
            str(response.context['income_all'][0].date), '2021-06-01')
        self.assertEqual(str(response.context['income_all'][0].comment), 'ква')
        self.assertEqual(response.context['income_all'][0].enabled, False)
        self.assertEqual(
            str(response.context['outcome_all'][0].type_of_transaction), 'OUT')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_section), 'Мои расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_category), 'Аптека')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_name), 'Антибиотики')
        self.assertEqual(
            str(response.context['outcome_all'][0].sum_money), '-500.00')
        self.assertEqual(
            str(response.context['outcome_all'][0].currency), 'BYN')
        self.assertEqual(
            str(response.context['outcome_all'][0].date), '2021-06-03')
        self.assertEqual(
            str(response.context['outcome_all'][0].comment), 'кря')
        self.assertEqual(response.context['outcome_all'][0].enabled, False)


class TestTransactionView(TestCase):
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

    def test_view_uses_correct_template_one_transaction_reports(self):
        resp = self.client.get(reverse('transaction_view', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/transaction_view.html')

    def test_correct_data_for_template_in_one_transaction_reports(self):
        response = self.client.get(
            reverse('detailed_current_financial_results'))
        self.assertEqual(
            str(response.context['outcome_all'][0].type_of_transaction), 'OUT')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_section), 'Мои расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_category), 'Мелкие расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_name), 'Магазин')
        self.assertEqual(
            str(response.context['outcome_all'][0].sum_money), '-5000.00')
        self.assertEqual(
            str(response.context['outcome_all'][0].currency), 'BYN')
        self.assertEqual(
            str(response.context['outcome_all'][0].date), '2021-06-01')
        self.assertEqual(
            str(response.context['outcome_all'][0].comment), 'ква')
        self.assertEqual(response.context['outcome_all'][0].enabled, False)


class TestTransactionUpdateView(TestCase):
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

    def test_view_uses_correct_template_transaction_update_reports(self):
        resp = self.client.get(reverse('transaction_update', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/transaction_update.html')

    def test_correct_data_for_template_in_transaction_update_reports(self):
        response = self.client.get(
            reverse('detailed_current_financial_results'))
        self.assertEqual(
            str(response.context['outcome_all'][0].type_of_transaction), 'OUT')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_section), 'Мои расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_category), 'Мелкие расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_name), 'Магазин')
        self.assertEqual(
            str(response.context['outcome_all'][0].sum_money), '-5000.00')
        self.assertEqual(
            str(response.context['outcome_all'][0].currency), 'BYN')
        self.assertEqual(
            str(response.context['outcome_all'][0].date), '2021-06-01')
        self.assertEqual(
            str(response.context['outcome_all'][0].comment), 'ква')
        self.assertEqual(response.context['outcome_all'][0].enabled, False)

    def test_correct_form_in_transaction_update_reports(self):
        response = self.client.get(reverse('transaction_update', args=[
            GeneralTable.objects.last().id]))
        self.assertIsInstance(
            response.context['form'], TransactionUpdateForm)


class TestTransactionDeleteView(TestCase):
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

    def test_view_uses_correct_template_transaction_delete_reports(self):
        resp = self.client.get(reverse('transaction_delete', args=[
                               GeneralTable.objects.last().id]))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, 'reports/transaction_delete.html')

    def test_correct_data_for_template_in_transaction_delete_reports(self):
        response = self.client.get(
            reverse('detailed_current_financial_results'))
        self.assertEqual(
            str(response.context['outcome_all'][0].type_of_transaction), 'OUT')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_section), 'Мои расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_category), 'Мелкие расходы')
        self.assertEqual(
            str(response.context['outcome_all'][0].id_name), 'Магазин')
        self.assertEqual(
            str(response.context['outcome_all'][0].sum_money), '-5000.00')
        self.assertEqual(
            str(response.context['outcome_all'][0].currency), 'BYN')
        self.assertEqual(
            str(response.context['outcome_all'][0].date), '2021-06-01')
        self.assertEqual(
            str(response.context['outcome_all'][0].comment), 'ква')
        self.assertEqual(response.context['outcome_all'][0].enabled, False)

    def test_correct_form_in_transaction_update_reports(self):
        response = self.client.get(reverse('transaction_delete', args=[
            GeneralTable.objects.last().id]))
        self.assertIsInstance(
            response.context['form'], TransactionDeleteForm)
