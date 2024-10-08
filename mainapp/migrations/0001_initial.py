# Generated by Django 5.0.7 on 2024-09-10 16:59

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('num_guests', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('notes', models.TextField(blank=True, null=True)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.table')),
            ],
        ),
    ]
