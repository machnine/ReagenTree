# Generated by Django 4.2.7 on 2023-12-22 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0047_rename_qunatity_unit_reagentcomponent_quantity_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='inhousereagent',
            name='product_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]