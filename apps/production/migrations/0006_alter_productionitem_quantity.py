# Generated by Django 5.0.2 on 2024-05-03 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_alter_productionitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionitem',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
