# Generated by Django 5.1.7 on 2025-03-25 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0011_alter_meeting_link'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name': 'Встреча', 'verbose_name_plural': 'Встречи'},
        ),
    ]
