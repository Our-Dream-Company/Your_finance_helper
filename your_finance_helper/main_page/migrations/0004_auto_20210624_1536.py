# Generated by Django 3.2.4 on 2021-06-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0003_auto_20210624_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=50, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='nameoperation',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
    ]