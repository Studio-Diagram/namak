# Generated by Django 2.1.5 on 2019-04-07 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounti', '0027_invoicessalestoshopproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField()),
                ('return_type', models.CharField(choices=[('CUSTOMER_TO_CAFE', 'مشتری به کافه'), ('CAFE_TO_SUPPLIER', 'کافه به تامین\u200cکننده')], max_length=50)),
                ('buy_price', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('numbers', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Branch')),
                ('shop_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.ShopProduct')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounti.Supplier')),
            ],
        ),
    ]
