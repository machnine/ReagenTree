# Generated by Django 5.0.1 on 2024-01-16 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_initial'),
        ('item', '0005_alter_inhousereagent_quantity_alter_item_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inhousereagent',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inhouse_reagents', to='category.category'),
        ),
    ]