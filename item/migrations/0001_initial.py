# Generated by Django 5.0 on 2023-12-28 20:47

import attachment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InhouseReagent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('product_id', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cas_number', models.CharField(blank=True, max_length=20, null=True)),
                ('product_id', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ItemAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to=attachment.models.UploadToPathAndRename('attachments'), verbose_name='file')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='uploaded at')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReagentComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ReagentValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('NOT_REQUIRED', 'Not Required')], default='PENDING', max_length=15)),
                ('validated', models.DateTimeField(auto_now_add=True)),
                ('authorised', models.DateTimeField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-validated'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_quantity', models.DecimalField(decimal_places=1, max_digits=10)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_condition', models.PositiveSmallIntegerField(choices=[(0, 'Unknown'), (1, 'Good'), (2, 'Unacceptable'), (3, 'Requires Attention')], default=0)),
                ('lot_number', models.CharField(max_length=50)),
                ('expiry_date', models.DateField()),
                ('created', models.DateTimeField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('ordinal_number', models.PositiveIntegerField(default=1)),
                ('total_count', models.PositiveIntegerField(default=1)),
                ('in_use_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
                'ordering': ['-created', '-ordinal_number'],
            },
        ),
        migrations.CreateModel(
            name='StockValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_quantity', models.DecimalField(decimal_places=1, max_digits=10)),
                ('used_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
