import datetime
from django.test import TestCase
from decimal import Decimal
from main_page.models import Section, Category, NameOperation, GeneralTable
from main_page.forms import AddIncomeForm, AddOutcomeForm, AddNewSectionForm, AddNewCategoryForm, AddNewNameForm
from django.urls import reverse


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        section_in = Section.objects.create(section="Основной доход")
        category_in = Category.objects.create(
            category="Работа", to_section=section_in)
        name_in = NameOperation.objects.create(
            name="Офис", to_category=category_in)
        GeneralTable.objects.create(
            type_of_transaction="IN",
            id_section=section_in,
            id_category=category_in,
            id_name=name_in,
            sum_money=Decimal('80000.00'),
            currency='BYN',
            date="2021-06-03",
            comment='доходики',
            enabled=False
        )
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
            comment='расходики',
            enabled=False
        )

    def test_view_uses_correct_template_main_page(self):
        resp = self.client.get(reverse('main_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/index.html')

    def test_view_correct_data_in_index_view(self):
        response = self.client.get(reverse('main_page'))
        self.assertTrue(
            'Основной доход' in response.context['in_dict_section'])
        self.assertTrue(
            'id_section__id' in response.context['in_dict_section']['Основной доход'])
        self.assertTrue(
            'Работа' in response.context['in_dict_category'])
        self.assertTrue(
            'id_category__id' in response.context['in_dict_category']['Работа'])
        self.assertTrue(
            'id_category__to_section' in response.context['in_dict_category']['Работа'])
        self.assertTrue('Офис' in response.context['in_dict_name'])
        self.assertTrue(
            'id_name__to_category' in response.context['in_dict_name']['Офис'])
        self.assertTrue('sum' in response.context['in_dict_name']['Офис'])
        self.assertEqual(response.context['in_sum_all'], Decimal('80000.00'))
        self.assertTrue(
            'Мои расходы' in response.context['out_dict_section'])
        self.assertTrue(
            'id_section__id' in response.context['out_dict_section']['Мои расходы'])
        self.assertTrue(
            'Мелкие расходы' in response.context['out_dict_category'])
        self.assertTrue(
            'id_category__id' in response.context['out_dict_category']['Мелкие расходы'])
        self.assertTrue(
            'id_category__to_section' in response.context['out_dict_category']['Мелкие расходы'])
        self.assertTrue('Магазин' in response.context['out_dict_name'])
        self.assertTrue(
            'id_name__to_category' in response.context['out_dict_name']['Магазин'])
        self.assertTrue('sum' in response.context['out_dict_name']['Магазин'])
        self.assertEqual(response.context['out_sum_all'], Decimal('-5000.00'))

        self.assertTrue(response.context['in_dict_section']['Основной доход']['id_section__id']
                        == response.context['in_dict_category']['Работа']['id_category__to_section'])
        self.assertTrue(response.context['in_dict_category']['Работа']['id_category__id']
                        == response.context['in_dict_name']['Офис']['id_name__to_category'])
        self.assertTrue(response.context['out_dict_section']['Мои расходы']['id_section__id']
                        == response.context['out_dict_category']['Мелкие расходы']['id_category__to_section'])
        self.assertTrue(response.context['out_dict_category']['Мелкие расходы']['id_category__id']
                        == response.context['out_dict_name']['Магазин']['id_name__to_category'])


class AddIncomeViewTest(TestCase):
    def test_view_uses_correct_template_add_income(self):
        resp = self.client.get(reverse('add_income'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_income.html')

    def test_published_post_add_income_transaction(self):
        self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        self.client.post(
            '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
        self.client.post(
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
        query = GeneralTable.objects.last()
        self.assertTrue(query.id_section, Section.objects.last().section)
        self.assertTrue(query.id_category, Category.objects.last().category)
        self.assertTrue(query.id_name, NameOperation.objects.last().name)
        self.assertEqual(query.type_of_transaction, "IN")
        self.assertEqual(query.sum_money, Decimal('50000.00'))
        self.assertEqual(query.currency, 'BYN')
        self.assertEqual(query.date, datetime.date(2021, 6, 1))
        self.assertEqual(query.comment, 'ква')
        self.assertEqual(query.enabled, False)
        self.assertEqual(len(GeneralTable.objects.all()), 1)
        self.assertRedirects(response_general_table_income,
                             '/', status_code=302)

    def test_correct_form_in_add_incomecome_transaction(self):
        response = self.client.get(reverse('add_income'))
        self.assertIsInstance(
            response.context['form'], AddIncomeForm)
        self.assertEqual(
            response.context['form'].instance.type_of_transaction, 'IN')


class AddOutcomeViewTest(TestCase):
    def test_view_uses_correct_template_add_outcome(self):
        resp = self.client.get(reverse('add_outcome'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_outcome.html')

    def test_published_post_add_outcome_transaction(self):
        self.client.post(
            '/add_new_section', {'section': "Мои расходы"})
        self.client.post(
            '/add_new_category', {'category': "Аптека", 'to_section': Section.objects.last().id})
        self.client.post(
            '/add_new_name', {'name': 'Антибиотики', 'to_category': Category.objects.last().id})
        response_general_table_outcome = self.client.post(
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
        query = GeneralTable.objects.last()
        self.assertTrue(query.id_section, Section.objects.last().section)
        self.assertTrue(query.id_category, Category.objects.last().category)
        self.assertTrue(query.id_name, NameOperation.objects.last().name)
        self.assertEqual(query.type_of_transaction, "OUT")
        self.assertEqual(query.sum_money, Decimal('-500.00'))
        self.assertEqual(query.currency, 'BYN')
        self.assertEqual(query.date, datetime.date(2021, 6, 3))
        self.assertEqual(query.comment, 'ква')
        self.assertEqual(query.enabled, False)
        self.assertEqual(len(GeneralTable.objects.all()), 1)
        self.assertRedirects(response_general_table_outcome,
                             '/', status_code=302)

    def test_correct_form_in_add_outcome_transaction(self):
        response = self.client.get(reverse('add_outcome'))
        self.assertIsInstance(
            response.context['form'], AddOutcomeForm)
        self.assertEqual(
            response.context['form'].instance.type_of_transaction, 'OUT')


class AddNewSectionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Section.objects.create(
            section="Семья",
            enabled_section=False
        )

    def test_view_uses_correct_template_add_new_section(self):
        resp = self.client.get(reverse('add_new_section'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_section.html')

    def test_published_post_add_new_section(self):
        response = self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        self.assertEqual(Section.objects.last().section, "Инвестиции")
        self.assertRedirects(response, '/add_new_section', status_code=302)

    def test_no_section_in_add_new_section(self):
        responce = Section.objects.last().section
        self.assertFalse(responce == 'Друзья')

    def test_non_existent_section_in_add_new_section(self):
        try:
            Section.objects.get(section='Здоровье')
        except:
            print('"Здоровье" section does not exist.')

    def test_post_without_data_in_add_new_section(self):
        try:
            self.client.post('/add_new_section', {'section': ''})
            self.assertEqual(Section.objects.last().section, '')
        except:
            print('Fill in the section field')

    def test_post_with_wrong_key_in_add_new_section(self):
        try:
            self.client.post('/add_new_section', {'category': 'Здоровье'})
            self.assertEqual(Section.objects.last().section, 'Здоровье')
        except:
            print('Wrong key for section')

    def test_correct_form_in_add_new_section(self):
        response = self.client.get(reverse('add_new_section'))
        self.assertIsInstance(
            response.context['form'], AddNewSectionForm)


class AddNewCategoryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        section = Section.objects.create(section="Спорт")
        Category.objects.create(
            category="Экипировка", to_section=section)

    def test_view_uses_correct_template_add_new_category(self):
        resp = self.client.get(reverse('add_new_category'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_category.html')

    def test_published_post_add_new_category(self):
        self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        response_category = self.client.post(
            '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
        self.assertEqual(Category.objects.last().category, "Банки")
        self.assertRedirects(
            response_category, '/add_new_category', status_code=302)

    def test_no_category_in_add_new_category(self):
        responce = Category.objects.last().category
        self.assertFalse(responce == 'Спортивное питание')

    def test_non_existent_category_in_add_new_category(self):
        try:
            Category.objects.get(category='Абонемент')
        except:
            print('"Абонемент" category does not exist.')

    def test_post_without_data_in_add_new_category(self):
        try:
            self.client.post('/add_new_section', {'section': "Инвестиции"})
            self.client.post(
                '/add_new_category', {'category': "", 'to_section': Section.objects.last().id})
            self.assertEqual(Category.objects.last().section, '')
        except:
            print('Fill in the category field')

    def test_post_with_wrong_key_in_add_new_category(self):
        try:
            self.client.post('/add_new_section',
                             {'section': "Дополнительный доход"})
            self.client.post(
                '/add_new_category', {'name': "Банки", 'to_section': Section.objects.last().id})
            self.assertEqual(Category.objects.last().section, 'Банки')
        except:
            print('Wrong key for category')

    def test_correct_form_in_add_new_category(self):
        response = self.client.get(reverse('add_new_category'))
        self.assertIsInstance(
            response.context['form'], AddNewCategoryForm)


class AddNewNameViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        section = Section.objects.create(section="Семья")
        category = Category.objects.create(
            category="Жена", to_section=section)
        NameOperation.objects.create(
            name="День Рождение", to_category=category)

    def test_view_uses_correct_template_add_new_name(self):
        resp = self.client.get(reverse('add_new_name'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main_page/add_new_name.html')

    def test_published_post_add_new_name_name(self):
        self.client.post(
            '/add_new_section', {'section': "Инвестиции"})
        self.client.post(
            '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
        response_name = self.client.post(
            '/add_new_name', {'name': 'Депозит', 'to_category': Category.objects.last().id})
        self.assertEqual(NameOperation.objects.last().name, "Депозит")
        self.assertRedirects(response_name, '/add_new_name', status_code=302)

    def test_no_name_in_add_new_name(self):
        responce = NameOperation.objects.last().name
        self.assertFalse(responce == 'Расходы')

    def test_non_existent_name_in_add_new_name(self):
        try:
            NameOperation.objects.get(name='Аптека')
        except:
            print('"Аптека" name does not exist.')

    def test_post_without_data_in_add_new_name(self):
        try:
            self.client.post(
                '/add_new_section', {'section': "Инвестиции"})
            self.client.post(
                '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
            self.client.post(
                '/add_new_name', {'name': '', 'to_category': Category.objects.last().id})
            self.assertEqual(NameOperation.objects.last().section, '')
        except:
            print('Fill in the name field')

    def test_post_with_wrong_key_in_add_new_name(self):
        try:
            self.client.post(
                '/add_new_section', {'section': "Инвестиции"})
            self.client.post(
                '/add_new_category', {'category': "Банки", 'to_section': Section.objects.last().id})
            self.client.post(
                '/add_new_name', {'sum_money': 'Депозит', 'to_category': Category.objects.last().id})
            self.assertEqual(Category.objects.last().section, 'Депозит')
        except:
            print('Wrong key for name')

    def test_correct_form_in_add_new_name(self):
        response = self.client.get(reverse('add_new_name'))
        self.assertIsInstance(
            response.context['form'], AddNewNameForm)
