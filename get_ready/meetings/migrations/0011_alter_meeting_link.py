# Generated by Django 5.1.7 on 2025-03-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0010_alter_meeting_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='link',
            field=models.URLField(blank=True, verbose_name='Ссылка на место, мероприятие'),
        ),
    ]
