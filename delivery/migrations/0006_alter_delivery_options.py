# Generated by Django 4.2.7 on 2023-12-15 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_delivery_created_delivery_created_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={'ordering': ['-delivery_date'], 'verbose_name': 'delivery', 'verbose_name_plural': 'deliveries'},
        ),
    ]
