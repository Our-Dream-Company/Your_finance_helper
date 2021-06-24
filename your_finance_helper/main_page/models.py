from django.db import models
from datetime import date


class Section(models.Model):
    section = models.CharField('Раздел', max_length=25)

    def __str__(self):
        return self.section

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    category = models.CharField('Категория', max_length=25, default='')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class NameOperation(models.Model):
    name = models.CharField('Наименование', max_length=25, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'


class GeneralTable(models.Model):
    class TypeOfTransaction(models.TextChoices):
        INCOME = 'IN', ('Income')
        OUTCOME = 'OUT', ('Outcome')

    type_of_transaction = models.CharField(
        choices=TypeOfTransaction.choices, default=TypeOfTransaction.OUTCOME, max_length=3)
    d_section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, verbose_name='Раздел')
    id_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    id_name = models.ForeignKey(
        NameOperation, on_delete=models.SET_NULL, null=True, verbose_name='Наименование')
    sum_money = models.DecimalField('Сумма', decimal_places=2, max_digits=10)
    date = models.DateField('Дата', default=date.today)
    comment = models.CharField('Комментарии', max_length=100, default='')
    on_delete = models.BooleanField('enabled', default=False)

    def __str__(self):
        return self.type_of_transaction

    class Meta:
        verbose_name = 'Главная таблица'
        verbose_name_plural = 'Главные таблицы'
