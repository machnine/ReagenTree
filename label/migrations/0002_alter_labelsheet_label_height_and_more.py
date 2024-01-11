# Generated by Django 5.0 on 2024-01-11 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labelsheet',
            name='label_height',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='label_width',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='margin_bottom',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='margin_left',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='margin_right',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='margin_top',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='space_x',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='labelsheet',
            name='space_y',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
