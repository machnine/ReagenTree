# Generated by Django 5.0.1 on 2024-01-24 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabelSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('page_size', models.CharField(choices=[('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'), ('LETTER', 'LETTER')], max_length=10)),
                ('label_width', models.FloatField()),
                ('label_height', models.FloatField()),
                ('label_rows', models.PositiveSmallIntegerField()),
                ('label_cols', models.PositiveSmallIntegerField()),
                ('margin_left', models.FloatField()),
                ('margin_right', models.FloatField()),
                ('margin_top', models.FloatField()),
                ('margin_bottom', models.FloatField()),
                ('space_x', models.FloatField()),
                ('space_y', models.FloatField()),
            ],
        ),
    ]
