# Generated by Django 5.2b1 on 2025-03-04 15:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='date_create',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date_meeting',
            field=models.DateField(verbose_name='Когда собираемся'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='link',
            field=models.URLField(blank=True, verbose_name='Ссылка на место, мероприятие'),
        ),
    ]
