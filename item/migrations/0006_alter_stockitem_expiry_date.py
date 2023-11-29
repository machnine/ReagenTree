# Generated by Django 4.2.7 on 2023-11-20 12:21

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_item_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='expiry_date',
            field=models.DateField(validators=[django.core.validators.MinValueValidator(datetime.date(2023, 11, 20))]),
        ),
    ]