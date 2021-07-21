# Generated by Django 3.2.4 on 2021-07-05 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0013_auto_20210705_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generaltable',
            name='id_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cat', to='main_page.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='generaltable',
            name='id_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nam', to='main_page.nameoperation', verbose_name='Name'),
        ),
    ]