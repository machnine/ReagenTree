# Generated by Django 4.2.7 on 2023-12-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_company_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]