# Generated by Django 2.1.5 on 2019-06-30 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounti', '0042_cash_ended_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='created_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
