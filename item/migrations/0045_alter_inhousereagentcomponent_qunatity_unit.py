# Generated by Django 4.2.7 on 2023-12-21 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0044_alter_stock_remaining_quantity_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inhousereagentcomponent',
            name='qunatity_unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.unit'),
        ),
    ]
