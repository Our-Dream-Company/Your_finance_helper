# Generated by Django 3.2.4 on 2021-06-24 11:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='generaltable',
            options={'verbose_name': 'General Table', 'verbose_name_plural': 'General Tables'},
        ),
        migrations.AlterModelOptions(
            name='nameoperation',
            options={'verbose_name': 'Name', 'verbose_name_plural': 'Names'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.RemoveField(
            model_name='generaltable',
            name='on_delete',
        ),
        migrations.AddField(
            model_name='generaltable',
            name='enabled',
            field=models.BooleanField(default=False, verbose_name='Enabled'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, max_length=25, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='comment',
            field=models.CharField(blank=True, max_length=100, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='d_section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_page.section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='id_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_page.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='id_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_page.nameoperation', verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='sum_money',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='type_of_transaction',
            field=models.CharField(choices=[('IN', 'Income'), ('OUT', 'Outcome')], max_length=3),
        ),
        migrations.AlterField(
            model_name='nameoperation',
            name='name',
            field=models.CharField(blank=True, max_length=25, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='section',
            name='section',
            field=models.CharField(max_length=25, verbose_name='Section'),
        ),
    ]
