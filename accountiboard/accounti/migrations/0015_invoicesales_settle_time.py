# Generated by Django 2.1.5 on 2019-03-12 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounti', '0014_invoicesales_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicesales',
            name='settle_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
