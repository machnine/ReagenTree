# Generated by Django 4.2.7 on 2023-11-19 20:20

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_description'),
        ('delivery', '0002_remove_delivery_condition'),
        ('company', '0002_alter_company_name'),
        ('item', '0002_stockitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockitem',
            name='in_use_date',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufactured_items', to='company.company'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='product_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplied_items', to='company.company'),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='delivery.delivery'),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='delivery_condition',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Unknown'), (1, 'Good'), (2, 'Unacceptable'), (3, 'Requires Attention')], default=0),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='expiry_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 11, 19))]),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_items', to='item.item'),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='lot_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]