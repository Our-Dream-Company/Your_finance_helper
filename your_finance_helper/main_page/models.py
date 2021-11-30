from django.contrib.auth.models import User
from django.db import models
from datetime import date

from django.http import request


class Section(models.Model):
    section = models.CharField('Section', max_length=50)
    enabled_section = models.BooleanField('Enabled', default=False)
    id_user_from_section = models.ForeignKey(
        User, related_name='user_section', on_delete=models.CASCADE, null=True, verbose_name='User')

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
    id_user_from_category = models.ForeignKey(
        User, related_name='user_category', on_delete=models.CASCADE, null=True, verbose_name='User')

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class NameOperation(models.Model):
    name_operation = models.CharField('Name Operation', max_length=50)
    to_category = models.ForeignKey(
        Category, related_name='to_cat', on_delete=models.SET_NULL, null=True, verbose_name='Category')
    enabled_name = models.BooleanField('Enabled', default=False)
    id_user_from_name_operation = models.ForeignKey(
        User, related_name='user_name_operation', on_delete=models.CASCADE, null=True, verbose_name='User')

    def __str__(self):
        return self.name_operation

    class Meta:
        verbose_name = 'Name Operation'
        verbose_name_plural = 'Names Operation'


class GeneralTable(models.Model):
    class TypeOfTransaction(models.TextChoices):
        INCOME = 'IN'
        OUTCOME = 'OUT'

    class Currency(models.TextChoices):
        BYN = 'BYN'
        USD = 'USD'
        EUR = 'EUR'
        RUR = 'RUR'
        PLZ = 'PLZ'

    type_of_transaction = models.CharField(
        choices=TypeOfTransaction.choices, max_length=3)
    id_section = models.ForeignKey(
        Section, related_name='sec', on_delete=models.CASCADE, null=True, verbose_name='Section')
    id_category = models.ForeignKey(
        Category, related_name='cat', on_delete=models.CASCADE, null=True, verbose_name='Category')
    id_name = models.ForeignKey(
        NameOperation, related_name='nam', on_delete=models.CASCADE, null=True, verbose_name='Name Operation')
    sum_money = models.DecimalField('Amount', decimal_places=2, max_digits=10)
    currency = models.CharField(
        choices=Currency.choices, max_length=3, default='BYN')
    date = models.DateField('Date', default=date.today)
    comment = models.CharField('Comment', max_length=100, blank=True)
    enabled = models.BooleanField('Enabled', default=False)
    id_user = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE, null=True, verbose_name='User')

    def __str__(self):
        return '{} {}'.format(self.type_of_transaction, self.id_section)

    class Meta:
        verbose_name = 'General Table'
        verbose_name_plural = 'General Tables'
