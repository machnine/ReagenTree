# Generated by Django 4.2.7 on 2023-11-19 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_alter_category_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
    ]
