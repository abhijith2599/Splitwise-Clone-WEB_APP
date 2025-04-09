# Generated by Django 5.1.6 on 2025-03-27 06:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Splitz', '0006_alter_splitmodel_expense_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SettlementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settled_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payed_on', models.DateField(auto_now_add=True)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
