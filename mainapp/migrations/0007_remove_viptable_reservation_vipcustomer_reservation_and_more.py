# Generated by Django 5.0.7 on 2024-09-13 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_viptable_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viptable',
            name='reservation',
        ),
        migrations.AddField(
            model_name='vipcustomer',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.vipreservation'),
        ),
        migrations.AddField(
            model_name='vipcustomer',
            name='vip_table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.viptable'),
        ),
    ]
