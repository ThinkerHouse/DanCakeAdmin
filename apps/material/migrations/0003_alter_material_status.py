# Generated by Django 5.0.2 on 2024-04-11 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_alter_material_material_type_alter_material_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='status',
            field=models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=0),
        ),
    ]
