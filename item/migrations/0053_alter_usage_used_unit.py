# Generated by Django 4.2.7 on 2023-12-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0052_usage_used_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='used_unit',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]