# Generated by Django 5.1.4 on 2025-01-05 13:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refill', '0007_alter_trip_trip_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='trip_price',
        ),
        migrations.AddField(
            model_name='vehicle_data',
            name='trip_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Price of the trip', max_digits=7, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
