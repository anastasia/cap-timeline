# Generated by Django 2.2.8 on 2019-12-16 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0002_event_timeline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relationship',
            old_name='preceding_event',
            new_name='event_one',
        ),
        migrations.RenameField(
            model_name='relationship',
            old_name='succeeding_event',
            new_name='event_two',
        ),
    ]
