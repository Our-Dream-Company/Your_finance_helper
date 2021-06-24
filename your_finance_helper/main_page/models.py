from django.db import models
from datetime import date


class Section(models.Model):
    section = models.CharField('Section', max_length=50)

    def __str__(self):
        return self.section

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'


class Category(models.Model):
    category = models.CharField('Category', max_length=50, null=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class NameOperation(models.Model):
    name = models.CharField('Name', max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Name'
        verbose_name_plural = 'Names'


class GeneralTable(models.Model):
    class TypeOfTransaction(models.TextChoices):
        INCOME = 'IN', ('Income')
        OUTCOME = 'OUT', ('Outcome')

    type_of_transaction = models.CharField(
        choices=TypeOfTransaction.choices, max_length=3)
    d_section = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True, verbose_name='Section')
    id_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name='Category')
    id_name = models.ForeignKey(
        NameOperation, on_delete=models.SET_NULL, null=True, verbose_name='Name')
    sum_money = models.DecimalField('Amount', decimal_places=2, max_digits=10)
    date = models.DateField('Date', default=date.today)
    comment = models.CharField('Comment', max_length=100, blank=True)
    enabled = models.BooleanField('Enabled', default=False)

    def __str__(self):
        return self.type_of_transaction

    class Meta:
        verbose_name = 'General Table'
        verbose_name_plural = 'General Tables'
