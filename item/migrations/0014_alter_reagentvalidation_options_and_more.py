# Generated by Django 5.0 on 2024-01-08 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0013_inhousereagentvalidation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reagentvalidation',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='reagentvalidation',
            old_name='validated',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='reagentvalidation',
            old_name='validated_by',
            new_name='created_by',
        ),
    ]
