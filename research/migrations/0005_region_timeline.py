# Generated by Django 2.2.8 on 2020-01-08 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0004_auto_20200108_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='timeline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='regions', to='research.Meta'),
        ),
    ]
