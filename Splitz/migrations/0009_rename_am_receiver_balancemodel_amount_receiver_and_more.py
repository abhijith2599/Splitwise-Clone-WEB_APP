# Generated by Django 5.1.6 on 2025-04-04 06:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Splitz', '0008_balancemodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='balancemodel',
            old_name='am_receiver',
            new_name='amount_receiver',
        ),
        migrations.AlterField(
            model_name='balancemodel',
            name='amount_payer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amount_payer', to=settings.AUTH_USER_MODEL),
        ),
    ]
