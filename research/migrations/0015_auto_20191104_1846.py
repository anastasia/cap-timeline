# Generated by Django 2.2.4 on 2019-11-04 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0014_auto_20191104_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relationship',
            old_name='head',
            new_name='preceding_event',
        ),
        migrations.RenameField(
            model_name='relationship',
            old_name='tail',
            new_name='succeeding_event',
        ),
    ]
