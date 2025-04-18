# Generated by Django 5.1.6 on 2025-04-02 06:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Splitz', '0007_settlementmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('am_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('amount_payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='am_payer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
