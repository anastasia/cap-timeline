# Generated by Django 2.2.4 on 2019-09-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0008_auto_20190829_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(blank=True, choices=[('us', 'us'), ('world', 'world'), ('legislation', 'legislation'), ('caselaw', 'caselaw')], max_length=100, null=True),
        ),
    ]
