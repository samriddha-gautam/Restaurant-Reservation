# Generated by Django 5.0.7 on 2024-09-13 09:40

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_table_is_occupied'),
    ]

    operations = [
        migrations.CreateModel(
            name='VIPCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('vip_since', models.DateField(default=datetime.date.today)),
                ('special_requests', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VipTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_occupied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VIPReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('num_guests', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('special_notes', models.TextField(blank=True, null=True)),
                ('vip_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.vipcustomer')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.viptable')),
            ],
        ),
    ]
