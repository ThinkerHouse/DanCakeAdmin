# Generated by Django 5.0.2 on 2024-04-28 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('received_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedorder',
            name='meta_data',
            field=models.JSONField(blank=True),
        ),
    ]
