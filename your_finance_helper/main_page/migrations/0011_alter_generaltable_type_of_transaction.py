# Generated by Django 3.2.4 on 2021-07-03 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0010_auto_20210703_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generaltable',
            name='type_of_transaction',
            field=models.CharField(choices=[('IN', 'Income'), ('OUT', 'Outcome')], max_length=7),
        ),
    ]
