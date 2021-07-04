from django.db import models
from datetime import date


class Section(models.Model):
    section = models.CharField('Section', max_length=50)
    enabled_section = models.BooleanField('Enabled', default=False)

    def __str__(self):
        return self.section

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'


class Category(models.Model):
    category = models.CharField('Category', max_length=50)
    to_section = models.ForeignKey(
        Section, related_name='to_sec', on_delete=models.SET_NULL, null=True, verbose_name='Section')
    enabled_category = models.BooleanField('Enabled', default=False)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class NameOperation(models.Model):
    name = models.CharField('Name', max_length=50)
    to_category = models.ForeignKey(
        Category, related_name='to_cat', on_delete=models.SET_NULL, null=True, verbose_name='Category')
    enabled_name = models.BooleanField('Enabled', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Name'
        verbose_name_plural = 'Names'


class GeneralTable(models.Model):
    class TypeOfTransaction(models.TextChoices):
        INCOME = 'IN', ('Income')
        OUTCOME = 'OUT', ('Outcome')

    class Currency(models.TextChoices):
        BYN = 'BYN', ('BYN')
        USD = 'USD', ('USD')
        EUR = 'EUR', ('EUR')
        RUR = 'RUR', ('RUR')
        PLZ = 'PLZ', ('PLZ')

    type_of_transaction = models.CharField(
        choices=TypeOfTransaction.choices, max_length=3)
    id_section = models.ForeignKey(
        Section, related_name='sec', on_delete=models.SET_NULL, null=True, verbose_name='Section')
    id_category = models.ForeignKey(
        Category, related_name='cat', on_delete=models.SET_NULL, null=True, verbose_name='Category')
    id_name = models.ForeignKey(
        NameOperation, related_name='nam', on_delete=models.SET_NULL, null=True,  verbose_name='Name')
    sum_money = models.DecimalField('Amount', decimal_places=2, max_digits=10)
    currency = models.CharField(
        choices=Currency.choices, max_length=3, default='BYN')
    date = models.DateField('Date', default=date.today)
    comment = models.CharField('Comment', max_length=100, blank=True)
    enabled = models.BooleanField('Enabled', default=False)

    def __str__(self):
        return self.type_of_transaction

    class Meta:
        verbose_name = 'General Table'
        verbose_name_plural = 'General Tables'
