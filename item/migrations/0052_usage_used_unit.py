# Generated by Django 4.2.7 on 2023-12-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0051_reagentvalidation'),
    ]

    operations = [
        migrations.AddField(
            model_name='usage',
            name='used_unit',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]
