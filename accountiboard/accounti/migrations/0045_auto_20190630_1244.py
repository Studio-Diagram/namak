# Generated by Django 2.1.5 on 2019-06-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounti', '0044_auto_20190630_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='end_working_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='start_working_time',
            field=models.TimeField(null=True),
        ),
    ]
