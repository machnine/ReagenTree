# Generated by Django 4.2.7 on 2023-11-21 21:34

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_alter_location_name'),
        ('item', '0007_alter_item_options_alter_stockitem_lot_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stockitems', to='location.location'),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='expiry_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 11, 21))]),
        ),
    ]
