# Generated by Django 4.2.7 on 2023-12-21 13:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0040_remove_stock_remaining_tests_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usage',
            old_name='usage_by',
            new_name='used_by',
        ),
        migrations.RenameField(
            model_name='usage',
            old_name='usage_date',
            new_name='used_date',
        ),
        migrations.RemoveField(
            model_name='usage',
            name='used_tests',
        ),
        migrations.RemoveField(
            model_name='usage',
            name='used_volume',
        ),
        migrations.RemoveField(
            model_name='usage',
            name='used_weight',
        ),
        migrations.AddField(
            model_name='usage',
            name='used_quantity',
            field=models.DecimalField(decimal_places=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity_unit',
            field=models.CharField(blank=True, choices=[('tests', 'tests'), ('μl', 'μl'), ('ml', 'ml'), ('L', 'L'), ('μg', 'μg'), ('mg', 'mg'), ('g', 'g'), ('kg', 'kg')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='remaining_quantity',
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
    ]