# Generated by Django 4.2.7 on 2023-12-27 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_alter_category_options'),
        ('item', '0063_rename_notes_reagentvalidation_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='inhousereagent',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inhouse_reagents', to='category.category'),
        ),
    ]
