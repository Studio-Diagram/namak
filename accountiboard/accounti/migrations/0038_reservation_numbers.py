# Generated by Django 2.1.5 on 2019-05-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounti', '0037_reservation_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='numbers',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
