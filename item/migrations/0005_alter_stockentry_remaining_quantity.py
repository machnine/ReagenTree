# Generated by Django 5.1.3 on 2024-11-19 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_alter_usage_used_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockentry',
            name='remaining_quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
