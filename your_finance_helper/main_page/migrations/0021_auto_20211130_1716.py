# Generated by Django 3.2.4 on 2021-11-30 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_page', '0020_auto_20211130_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id_user_from_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_category', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='nameoperation',
            name='id_user_from_name_operation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_name_operation', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='section',
            name='id_user_from_section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_section', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
